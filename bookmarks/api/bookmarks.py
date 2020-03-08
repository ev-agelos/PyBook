"""API endpoints for bookmarks."""

from flask import request, jsonify, Blueprint, url_for, g

from bookmarks import csrf
from bookmarks.models import Bookmark, Favourite, BookmarkSchema, VoteSchema
from bookmarks.forms import AddBookmarkForm, UpdateBookmarkForm
from bookmarks.logic import _get, _post, _put, _delete, _save, _unsave

from .auth import token_auth

bookmarks_api = Blueprint('bookmarks_api', __name__)
csrf.exempt(bookmarks_api)


@bookmarks_api.route('/api/bookmarks/')
@bookmarks_api.route('/api/bookmarks/<int:id>')
@token_auth.login_required
def get(id=None):
    """Return all bookmarks."""
    if id is None:
        query = _get()
        bookmarks = BookmarkSchema().dump(query.all(), many=True)
        return jsonify(bookmarks=bookmarks), 200
    else:
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            return jsonify(message='Bookmark not found', status=404), 404
        return BookmarkSchema().jsonify(bookmark), 200


@bookmarks_api.route('/api/bookmarks/', methods=['POST'])
@token_auth.login_required
def post():
    """Add new bookmark and add it's tags if don't exist."""
    form = AddBookmarkForm(meta={'csrf':False})
    if not form.validate():
        return jsonify(message='invalid data', status=400), 400
    bookmark = Bookmark.query.filter_by(url=form.url.data).scalar()
    if bookmark is not None:
        return jsonify(message='bookmark already exists', status=409), 409
    bookmark_id = _post(form)

    response = jsonify({})
    response.status_code = 201
    response.headers['Location'] = url_for(
        'bookmarks_api.get', id=bookmark_id, _external=True)
    return response


@bookmarks_api.route('/api/bookmarks/<int:id>', methods=['PUT'])
@token_auth.login_required
def put(id):
    """
    Update a bookmark entry.

    In case tag(s) changes check if no other bookmark is related with
    that tag(s) and if not, delete it.
    """
    form = UpdateBookmarkForm(meta={'csrf':False})
    if not form.validate():
        return jsonify(message='invalid data', status=400), 400
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='Bookmark does not exist', status=404), 404
    if form.url.data and form.url.data != bookmark.url:
        existing_url = Bookmark.query.filter_by(url=form.url.data).scalar()
        if existing_url is not None:
            return jsonify(message='url already exists', status=409), 409
    _put(id, form)
    return jsonify(message='Bookmark updated', status=200), 200


@bookmarks_api.route('/api/bookmarks/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete(id):
    """Delete a bookmark."""
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='not found', status=404), 404
    if bookmark.user_id != g.user.id:
        return jsonify(message='forbidden', status=403), 403
    _delete(id)
    return jsonify({}), 204


@bookmarks_api.route('/api/bookmarks/<int:id>/save', methods=['POST'])
@token_auth.login_required
def save(id):
    """Save a bookmark to user's saved listings."""
    if Bookmark.query.get(id) is None:
        return jsonify(message='bookmark not found', status=404), 404
    elif Favourite.query.filter_by(user_id=g.user.id,
                                   bookmark_id=id).scalar() is not None:
        return jsonify(message='bookmark already saved', status=409), 409
    _save(id)
    response = jsonify({})
    response.status_code = 201
    return response


@bookmarks_api.route('/api/bookmarks/<int:id>/unsave', methods=['DELETE'])
@token_auth.login_required
def unsave(id):
    """Un-save a bookmark from user's saved listings."""
    if Bookmark.query.get(id) is None:
        return jsonify(message='bookmark not found', status=404), 404
    favourite = Favourite.query.filter_by(user_id=g.user.id,
                                          bookmark_id=id).scalar()
    if favourite is None:
        return jsonify(message='save not found', status=404), 404
    _unsave(favourite)
    return jsonify({}), 204


@bookmarks_api.route('/api/bookmarks/<int:id>/votes')
@token_auth.login_required
def get_votes(id):
    """Return all votes for a bookmark."""
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='not found', status=404), 404

    votes = bookmark.votes
    user_id = request.args.get('user_id', type=int)
    if user_id:
        votes = votes.filter_by(user_id=user_id)
    votes_ = VoteSchema().dump(votes.all(), many=True)
    return jsonify(votes=votes_), 200
