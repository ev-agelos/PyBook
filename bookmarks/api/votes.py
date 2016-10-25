"""API endpoints for votes."""

from flask import request, Blueprint, url_for, g

from bookmarks import csrf

from .auth import token_auth
from ..logic import _post_vote, _put_vote, _delete_vote


votes_api = Blueprint('votes_api', __name__)
csrf.exempt(votes_api)


@votes_api.route('/api/vote', methods=['POST', 'PUT', 'DELETE'])
@token_auth.login_required
def vote():
    """Add a new vote for a bookmark."""
    bookmark_id = request.get_json().get('bookmark_id')
    if request.method == 'POST':
        response = _post_vote(bookmark_id)
        response.headers['Location'] = url_for(
            'bookmarks_api.get_votes', bookmark_id=bookmark_id,
            user_id=g.user.id, _external=True)
        return response
    elif request.method == 'PUT':
        return _put_vote(bookmark_id)
    else:
        return _delete_vote(bookmark_id)
