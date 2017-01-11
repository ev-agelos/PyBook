"""API endpoints for bookmarks."""

from flask import request, jsonify, Blueprint, url_for, g

from bookmarks import csrf
from bookmarks.models import Bookmark, BookmarkSchema, VoteSchema
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
        bookmarks = BookmarkSchema().dump(query.all(), many=True).data
        return jsonify(bookmarks=bookmarks), 200
    else:
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            return jsonify(message='Bookmark not found', status=404), 404
        return BookmarkSchema().jsonify(bookmark), 200


@bookmarks_api.route('/api/bookmarks/', methods=['POST'])
@token_auth.login_required
def post():
    """Add new bookmark and add it's category if does not exist."""
    form = AddBookmarkForm(csrf_enabled=False)
    return _post(form)


@bookmarks_api.route('/api/bookmarks/<int:id>', methods=['PUT'])
@token_auth.login_required
def put(id):
    """
    Update a bookmark entry.

    In case category changes check if no other bookmark is related with
    that category and if not, delete it.
    """
    form = UpdateBookmarkForm(csrf_enabled=False)
    return _put(id, form)


@bookmarks_api.route('/api/bookmarks/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete(id):
    """Delete a bookmark."""
    return _delete(id)


@bookmarks_api.route('/api/bookmarks/<int:id>/save', methods=['POST'])
@token_auth.login_required
def save(id):
    """Save a bookmark to user's saved listings."""
    return _save(id)


@bookmarks_api.route('/api/bookmarks/<int:id>/unsave', methods=['DELETE'])
@token_auth.login_required
def unsave(id):
    """Un-save a bookmark from user's saved listings."""
    return _unsave(id)


@bookmarks_api.route('/api/bookmarks/<int:id>/votes')
@token_auth.login_required
def get_votes(id):
    """Return all votes for a bookmark."""
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='not found', status=404), 404

    votes = bookmark.votes
    user_id = request.args.get('user_id')
    if user_id:
        votes.filter_by(user_id=user_id)
    votes_ = VoteSchema().dump(votes.all(), many=True).data
    return jsonify(votes=votes_), 200
