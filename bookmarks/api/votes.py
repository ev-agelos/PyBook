"""API endpoints for votes."""

from flask import request, Blueprint, url_for, g, jsonify

from bookmarks import csrf
from bookmarks.models import Bookmark, Vote, VoteSchema
from .auth import token_auth
from ..logic import _post_vote, _put_vote, _delete_vote


votes_api = Blueprint('votes_api', __name__)
csrf.exempt(votes_api)


@votes_api.route('/api/vote', methods=['POST', 'PUT', 'DELETE'])
@token_auth.login_required
def vote():
    """Add a new vote for a bookmark."""
    payload = request.get_json() or {}
    bookmark_id = payload.get('bookmark_id')
    if request.method in ('POST', 'PUT'):
        vote_arg = payload.get('vote')
        direction = {1: True, -1: False}.get(vote_arg)
        if direction is None:
            return jsonify(message='invalid data', status=400), 400
    if request.method in ('POST', 'DELETE') and \
            not isinstance(bookmark_id, int):
        return jsonify(message='invalid bookmark_id', status=400), 400

    if request.method == 'POST':
        bookmark = Bookmark.query.get(bookmark_id)
        if bookmark is None:
            return jsonify(message='bookmark not found', status=404), 404
        if Vote.query.filter_by(bookmark_id=bookmark_id,
                                user_id=g.user.id).scalar() is not None:
            return jsonify(message='vote already exists', status=409), 409
        _post_vote(bookmark, direction, vote_arg)
        response = jsonify({})
        response.status_code = 201
        response.headers['Location'] = url_for(
            'bookmarks_api.get_votes', bookmark_id=bookmark_id,
            user_id=g.user.id, _external=True)
        return response
    elif request.method == 'PUT':
        vote_ = Vote.query.filter_by(user_id=g.user.id,
                                     bookmark_id=bookmark_id).scalar()
        if vote_ is None:
            return jsonify(message='vote not found', status=404), 404
        if direction == vote_.direction:
            return jsonify(message='bookmark is voted with {} already'
                           .format('+1' if direction == 1 else '-1'),
                           status=409), 409
        _put_vote(vote_, direction, vote_arg)
        return VoteSchema().jsonify(vote_), 200
    else:
        vote = Vote.query.filter_by(user_id=g.user.id,
                                    bookmark_id=bookmark_id).scalar()
        if vote is None:
            return jsonify(message='no vote found for the given bookmark_id',
                           status=404), 404
        if vote.user_id != g.user.id:
            return jsonify(message='forbidden', status=403), 403
        _delete_vote(vote)
        return jsonify({}), 204
