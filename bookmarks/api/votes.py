"""API endpoints for votes."""

from flask import url_for, g
from flask.views import MethodView
from flask_login import login_required
from flask_smorest import Blueprint, abort

from bookmarks import csrf
from bookmarks.models import Bookmark, Vote
from .schemas import VoteSchema, VotePOSTSchema, VotePUTSchema
from ..logic import _post_vote, _put_vote, _delete_vote


votes_api = Blueprint('votes_api', 'Votes', url_prefix='/api/v1/votes/',
                      description='Operations on Votes')


@votes_api.route('/')
class VotesAPI(MethodView):

    decorators = [login_required, csrf.exempt]

    @votes_api.response(VoteSchema(many=True))
    def get(self):
        """Get all votes."""
        return Vote.query.filter_by(user_id=g.user.id).all()

    @votes_api.arguments(VotePOSTSchema)
    def post(self, data):
        """Add a new vote for a bookmark."""
        if Vote.query.filter_by(user_id=g.user.id, bookmark_id=data['bookmark_id']).scalar():
            abort(409, message='Vote already exists')
        bookmark = Bookmark.query.get(data['bookmark_id'])
        if bookmark is None:
            abort(404, message='Bookmark not found')

        vote_id = _post_vote(bookmark, data['direction'])
        vote_url = url_for(
            'votes_api.VoteAPI',
            id=vote_id,
            _method='GET',
            _external=True
        )
        return {}, 201, {'Location': vote_url}


@votes_api.route('/<int:id>')
class VoteAPI(MethodView):

    decorators = [login_required, csrf.exempt]

    @votes_api.response(VoteSchema())
    def get(self, id):
        vote = Vote.query.get(id)
        if vote.user != g.user:
            abort(403, message='forbidden')
        return vote or abort(404, message='Vote not found')

    @votes_api.arguments(VotePUTSchema)
    def put(self, data, id):
        """Update an existing vote for a bookmark."""
        vote = Vote.query.get(id)
        if vote is None:
            abort(404, message='Vote not found')
        if vote.user != g.user:
            abort(403, message='forbidden')
        _put_vote(vote, data['direction'])
        vote_url = url_for(
            'votes_api.VoteAPI',
            id=vote.id,
            _method='GET',
            _external=True
        )
        return {}, 204, {'Location': vote_url}

    @votes_api.response(code=204)
    def delete(self, id):
        """Delete a vote for a bookmark."""
        vote = Vote.query.get(id)
        if vote is None:
            abort(404, message='Vote not found')
        if vote.user != g.user:
            abort(403, message='forbidden')
        _delete_vote(vote)
