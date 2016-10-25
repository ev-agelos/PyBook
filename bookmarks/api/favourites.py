"""API endpoints for favorites."""

from flask import request, Blueprint, jsonify, url_for, g

from bookmarks import csrf

from .auth import token_auth
from ..logic import _save, _unsave


favourites_api = Blueprint('favourites_api', __name__)
csrf.exempt(favourites_api)


@favourites_api.route('/api/save', methods=['POST'])
@token_auth.login_required
def save():
    """Save a bookmark to user's saved listings."""
    bookmark_id = request.args.get('bookmark_id')
    response = _save(bookmark_id)
    # FIXME below is wrong, it should be something like:
    # /users/3/favourites/1 OR /users/3/favourites and be a list with 1 entry
    response.headers['Location'] = url_for('users_api.get_favourites',
                                           id=g.user.id, _external=True)
    return response


@favourites_api.route('/api/unsave', methods=['DELETE'])
@token_auth.login_required
def unsave():
    """Un-save a bookmark from user's saved listings."""
    bookmark_id = request.args.get('bookmark_id')
    return _unsave(bookmark_id)
