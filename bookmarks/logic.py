"""The logic around bookmarks so both api and regular views share."""


from flask import jsonify, url_for, g, request
from sqlalchemy.sql.expression import asc, desc

from bookmarks import db
from bookmarks.views.utils import get_url_thumbnail
from .models import Bookmark, Category, Vote, Favourite, VoteSchema

SORTS = {'date': desc(Bookmark.created_on), '-date': asc(Bookmark.created_on),
         'rating': desc(Bookmark.rating), '-rating': asc(Bookmark.rating)}


def _get(id=None):
    """
    Return the query for the bookmark with the given id or all bookmarks.

    This function returns the query comparing to other functions because the
    regular view paginates the query where the api view applies schema in order
    to return the result in json.
    """
    if id is None:
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
    if not form.validate():
        return jsonify(message='invalid data', status=400), 400

    category_ = form.category.data.lower() or 'uncategorized'
    bookmark = Bookmark.query.filter_by(url=form.url.data).scalar()
    if bookmark is not None:
        return jsonify(message='bookmark already exists', status=409), 409

    category = Category.query.filter_by(name=category_).scalar()
    if category is None:
        category = Category(name=category_)
    bookmark = Bookmark(title=form.title.data, url=form.url.data,
                        user_id=g.user.id, category=category,
                        image=get_url_thumbnail(form.url.data))
    db.session.add(bookmark)
    db.session.commit()
    response = jsonify({})
    response.status_code = 201
    response.headers['Location'] = url_for(
        'bookmarks_api.get', id=bookmark.id, _external=True)
    return response


def _put(id, form):
    """Update bookmark with the given form data."""
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='Bookmark does not exist', status=404), 404

    if not form.validate():
        return jsonify(message='invalid data', status=400), 400

    if form.url.data and form.url.data != bookmark.url:
        existing_url = Bookmark.query.filter_by(url=form.url.data).scalar()
        if existing_url is not None:
            return jsonify(message='url already exists', status=409), 409
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

    return jsonify(message='Bookmark updated', status=200), 200


def _delete(id):
    """Delete a bookmark."""
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='not found', status=404), 404
    if bookmark.user_id != g.user.id:
        return jsonify(message='forbidden', status=403), 403
    # Delete associated categories
    if Bookmark.query.filter_by(category_id=bookmark.category_id).count() == 1:
        db.session.delete(bookmark.category)
    # Delete associated votes
    db.session.query(Vote).filter_by(bookmark_id=id).delete()
    # Delete associated saves
    db.session.query(Favourite).filter_by(bookmark_id=id).delete()
    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), 204


def _save(id):
    """Save a bookmark to user's listings."""
    if not id:
        return jsonify(message='invalid data', status=400), 400
    favourite = Favourite.query.filter_by(user_id=g.user.id,
                                          bookmark_id=id).scalar()
    if favourite is not None:
        return jsonify(message='bookmark already saved', status=409), 409

    favourite = Favourite(user_id=g.user.id, bookmark_id=id)
    db.session.add(favourite)
    db.session.commit()
    response = jsonify({})
    response.status_code = 201
    return response


def _unsave(id):
    """Remove saved bookmark from user's listings."""
    if not id:
        return jsonify(message='invalid data', status=400), 400
    favourite = Favourite.query.filter_by(user_id=g.user.id,
                                          bookmark_id=id).scalar()
    if favourite is None:
        return jsonify(message='save not found', status=404), 404
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({}), 204


def _create_vote(bookmark_id, direction):
    """Helper function for adding new vote."""
    vote = Vote(user_id=g.user.id, bookmark_id=bookmark_id,
                direction=direction)
    db.session.add(vote)
    db.session.commit()

    response = jsonify({})
    response.status_code = 201
    return response


def _post_vote(bookmark_id):
    """Create a new vote entry."""
    vote_arg = request.get_json().get('vote')
    vote = {1: True, -1: False}.get(vote_arg)
    if vote is None or not bookmark_id:
        return jsonify(message='invalid data', status=400), 400

    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark is None:
        return jsonify(message='bookmark not found', status=404), 404

    if Vote.query.filter_by(bookmark_id=bookmark_id,
                            user_id=g.user.id).scalar() is not None:
        return jsonify(message='vote already exists', status=409), 409

    bookmark.rating += vote_arg
    db.session.add(bookmark)
    db.session.commit()
    return _create_vote(bookmark_id, vote)


def _put_vote(bookmark_id):
    """Update an existing vote."""
    vote_arg = request.get_json().get('vote')
    vote = {1: True, -1: False}.get(vote_arg)
    if vote is None:
        return jsonify(message='invalid vote', status=400), 400
    if not bookmark_id:
        return jsonify(message='invalid bookmark_id', status=400), 400
    vote_ = Vote.query.filter_by(user_id=g.user.id,
                                 bookmark_id=bookmark_id).scalar()
    if vote_ is None:
        return jsonify(message='vote not found', status=404), 404
    if vote == vote_.direction:
        return jsonify(message='bookmark is voted with {} already'.format(
            '+1' if vote == 1 else '-1'), status=409), 409

    vote_.direction = vote
    bookmark = Bookmark.query.get(bookmark_id)
    bookmark.rating += vote_arg * 2
    db.session.add(vote_)
    db.session.add(bookmark)
    db.session.commit()

    return VoteSchema().jsonify(vote_), 200


def _delete_vote(bookmark_id):
    """Delete an existing vote."""
    if not bookmark_id:
        return jsonify(message='invalid bookmark_id', status=400), 400
    vote = Vote.query.filter_by(user_id=g.user.id,
                                bookmark_id=bookmark_id).scalar()
    if vote is None:
        return jsonify(message='no vote found for the given bookmark_id',
                       status=404), 404
    if vote.user_id != g.user.id:
        return jsonify(message='forbidden', status=403), 403

    vote.bookmark.rating += 1 if not vote.direction else -1
    db.session.add(vote.bookmark)
    db.session.delete(vote)
    db.session.commit()
    return jsonify({}), 204
