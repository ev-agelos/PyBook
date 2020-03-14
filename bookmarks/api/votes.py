"""API endpoints for votes."""

from flask import request, url_for, g, jsonify
from flask.views import MethodView

from bookmarks import csrf
from bookmarks.models import Bookmark, Vote, VoteSchema
from .auth import token_auth
from ..logic import _post_vote, _put_vote, _delete_vote


class VotesAPI(MethodView):
    """Get/Add/Update/Delete a vote for a bookmark."""

    decorators = [token_auth.login_required, csrf.exempt]

    def get(self, id=None):
        """Get all user's votes."""
        if id is not None:
            vote = Vote.query.get(id)
            if vote is None:
                return jsonify(message='Vote not found', status=404), 404
            if vote.user != g.user:
                return jsonify(message='forbidden', status=403), 403
            return VoteSchema().jsonify(vote), 200

        query = Vote.query
        if 'bookmark_id' in request.args:
            if Bookmark.query.get(request.args['bookmark_id']) is None:
                return jsonify(message='Bookmark not found'), 404
            query = query.filter_by(bookmark_id=request.args['bookmark_id'])
        query = query.filter_by(user_id=g.user.id)

        votes = VoteSchema().dump(query.all(), many=True)
        return jsonify(votes=votes), 200


    def post(self):
        """Add a new vote for a bookmark."""
        payload = request.get_json() or {}
        if not payload:
            return jsonify(message='bad data', status=400), 400
        vote_arg = payload.get('vote')
        direction = {1: True, -1: False}.get(vote_arg)
        if direction is None:
            return jsonify(message='invalid data', status=400), 400

        bookmark_id = payload.get('bookmark_id')
        bookmark = Bookmark.query.get(bookmark_id)
        if bookmark is None:
            return jsonify(message='bookmark not found', status=404), 404

        if Vote.query.filter_by(bookmark_id=bookmark_id, user_id=g.user.id).scalar():
            return jsonify(message='vote already exists', status=409), 409

        vote_id = _post_vote(bookmark, direction, vote_arg)
        response = jsonify({})
        response.status_code = 201
        response.headers['Location'] = url_for(
            'votes_api',
            id=vote_id,
            _method='GET',
            _external=True
        )
        return response

    def put(self, id):
        """Update an existing vote for a bookmark."""
        payload = request.get_json() or {}
        if not payload:
            return jsonify(message='bad data', status=400), 400
        vote = Vote.query.get(id)
        if vote is None:
            return jsonify(message='vote not found', status=404), 404
        if vote.user != g.user:
            return jsonify(message='forbidden', status=403), 403

        vote_arg = payload.get('vote')
        direction = {1: True, -1: False}.get(vote_arg)
        if direction is None:
            return jsonify(message='invalid data', status=400), 400
        if direction == vote.direction:
            return jsonify(message='bookmark is voted with {} already'
                           .format('+1' if direction == 1 else '-1'),
                           status=409), 409
        _put_vote(vote, direction, vote_arg)
        return VoteSchema().jsonify(vote), 200

    def delete(self, id):
        """Delete a vote for a bookmark."""
        vote = Vote.query.get(id)
        if vote is None:
            return jsonify(message='vote not found', status=404), 404
        if vote.user != g.user:
            return jsonify(message='forbidden', status=403), 403
        _delete_vote(vote)
        return jsonify({}), 204


votes_api = VotesAPI.as_view('votes_api')
