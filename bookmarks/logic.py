"""The logic around bookmarks so both api and regular views share."""


from flask import g, request
from sqlalchemy.sql.expression import asc, desc

from bookmarks import db
from bookmarks.views import utils
from .models import Bookmark, Tag, tags_bookmarks, Vote, Favourite

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
    if request.args.get('tag'):
        tag = Tag.query.filter_by(
            name=request.args.get('tag').lower()).scalar()
        if tag is not None:
            query = query.join(tags_bookmarks).filter_by(tag_id=tag.id)

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
    bookmark = Bookmark(title=form.title.data, url=form.url.data,
                        user_id=g.user.id)
    for string in form.tags.data:
        tag = Tag.query.filter_by(name=string.lower()).scalar()
        if tag is None:
            tag = Tag(name=string.lower())
            db.session.add(tag)
        bookmark.tags.append(tag)

    db.session.add(bookmark)
    db.session.commit()
    utils.get_url_thumbnail(form.url.data, bookmark.id)
    return bookmark.id


def _put(id, form):
    """Update bookmark with the given form data."""
    bookmark = Bookmark.query.get(id)
    if form.url.data and form.url.data != bookmark.url:
        bookmark.url = form.url.data
    if form.title.data and form.title.data != bookmark.title:
        bookmark.title = form.title.data

    given_tags = {string.lower() for string in form.tags.data}
    linked_tags = {tag.name: tag for tag in bookmark.tags}
    tags_to_del = set(linked_tags.keys()) - given_tags
    tags_to_add = given_tags - set(linked_tags.keys())
    if given_tags != set(linked_tags.keys()):
        for name in tags_to_del:  # un-link not given tags
            tag_to_del = linked_tags[name]
            if db.session.query(tags_bookmarks).filter_by(
                    tag_id=tag_to_del.id).count() == 1:
                db.session.delete(tag_to_del)
            bookmark.tags.remove(tag_to_del)

        existing = Tag.query.filter(Tag.name.in_(tags_to_add)).all()
        existing_tags = {tag.name: tag for tag in existing}
        for new_string in tags_to_add:  # link the given tags
            tag = existing_tags.get(new_string, Tag(name=new_string))
            bookmark.tags.append(tag)

    db.session.add(bookmark)
    db.session.commit()


def _delete(id):
    """Delete a bookmark."""
    bookmark = Bookmark.query.get(id)
    # Delete associated tags
    for tag in bookmark.tags:
        if db.session.query(tags_bookmarks).filter_by(
                tag_id=tag.id).count() == 1:
            db.session.delete(tag)
    db.session.delete(bookmark)
    db.session.commit()


def _save(bookmark_id):
    """Save a bookmark to user's listings."""
    favourite = Favourite(bookmark_id=bookmark_id, user_id=g.user.id)
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
