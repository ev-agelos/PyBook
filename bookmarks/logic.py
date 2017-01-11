"""The logic around bookmarks so both api and regular views share."""


from flask import g, request
from sqlalchemy.sql.expression import asc, desc

from bookmarks import db
from bookmarks.views import utils
from .models import Bookmark, Category, Vote, Favourite

SORTS = {'date': desc(Bookmark.created_on), '-date': asc(Bookmark.created_on),
         'rating': desc(Bookmark.rating), '-rating': asc(Bookmark.rating)}


def _get():
    """
    Return the query for all bookmarks.

    This function returns the query comparing to other functions because the
    regular view paginates the query where the api view applies schema in order
    to return the result in json.
    """
    query = Bookmark.query
    if request.args.get('category'):
        category = Category.query.filter_by(
            name=request.args.get('category').lower()).scalar()
        if category is not None:
            query = query.filter_by(category=category)

    if request.args.get('sort'):
        sort_args = request.args.get('sort', '').lower().split(',')
        for sort in sort_args:
            if sort in SORTS:
                query = query.order_by(SORTS[sort])
    else:  # sort newest as default sorting
        query = query.order_by(SORTS['date'])
    return query


def _post(form):
    """Add a new bookmark according to the given form data."""
    category_ = form.category.data.lower() or 'uncategorized'
    category = Category.query.filter_by(name=category_).scalar()
    if category is None:
        category = Category(name=category_)
    bookmark = Bookmark(title=form.title.data, url=form.url.data,
                        user_id=g.user.id, category=category,
                        image=utils.get_url_thumbnail(form.url.data))
    db.session.add(bookmark)
    db.session.commit()
    return bookmark.id


def _put(id, form):
    """Update bookmark with the given form data."""
    bookmark = Bookmark.query.get(id)
    if form.url.data and form.url.data != bookmark.url:
        bookmark.url = form.url.data

    if form.category.data and \
            form.category.data.lower() != bookmark.category.name:
        existing_category = Category.query.filter_by(
            name=form.category.data.lower()).scalar()
        if existing_category is None:
            # Delete old category if no bookmarks are related with
            if bookmark.category.bookmarks.count() == 1:
                db.session.delete(bookmark.category)
            bookmark.category = Category(name=form.category.data.lower())
        else:
            bookmark.category = existing_category

    if form.title.data and form.title.data != bookmark.title:
        bookmark.title = form.title.data
    db.session.add(bookmark)
    db.session.commit()


def _delete(id):
    """Delete a bookmark."""
    bookmark = Bookmark.query.get(id)
    # Delete associated categories
    if Bookmark.query.filter_by(category_id=bookmark.category_id).count() == 1:
        db.session.delete(bookmark.category)
    # Delete associated votes
    db.session.query(Vote).filter_by(bookmark_id=id).delete()
    # Delete associated saves
    db.session.query(Favourite).filter_by(bookmark_id=id).delete()
    db.session.delete(bookmark)
    db.session.commit()


def _save(favourite):
    """Save a bookmark to user's listings."""
    db.session.add(favourite)
    db.session.commit()


def _unsave(favourite):
    """Remove saved bookmark from user's listings."""
    db.session.delete(favourite)
    db.session.commit()


def _post_vote(bookmark, direction, vote_arg):
    """Create a new vote entry."""
    bookmark.rating += vote_arg
    vote = Vote(user_id=g.user.id, bookmark_id=bookmark.id,
                direction=direction)
    db.session.add(bookmark)
    db.session.add(vote)
    db.session.commit()


def _put_vote(vote_, direction, vote_arg):
    """Update an existing vote."""
    vote_.direction = direction
    bookmark = Bookmark.query.get(vote_.bookmark_id)
    bookmark.rating += vote_arg * 2
    db.session.add(vote_)
    db.session.add(bookmark)
    db.session.commit()


def _delete_vote(vote):
    """Delete an existing vote."""
    vote.bookmark.rating += 1 if not vote.direction else -1
    db.session.add(vote.bookmark)
    db.session.delete(vote)
    db.session.commit()
