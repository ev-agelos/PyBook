"""API endpoints for users."""


from flask import g, jsonify, Blueprint

from bookmarks import db
from bookmarks.models import FavouriteSchema, VoteSchema
from bookmarks.users.models import User, UserSchema

from .auth import token_auth

users_api = Blueprint('users_api', __name__)


@users_api.route('/api/users/')
@users_api.route('/api/users/<int:id>')
@token_auth.login_required
def get(id=None):
    """Get a user given an id or get all users."""
    if id is None:
        users = UserSchema().dump(User.query.all(), many=True).data
        return jsonify(users=users), 200
    if id != g.user.id:
        user = User.query.get(id)
        if user is None:
            return jsonify(message='not found', status=404), 404
        return UserSchema().jsonify(user), 200
    return UserSchema().jsonify(g.user), 200


@users_api.route('/api/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def put(id):
    """Update an existing user."""
    # TODO need to make a form to avoid validation checks
    pass


@users_api.route('/api/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete(id):
    """Delete an existing user, his favourites and saves."""
    if id != g.user.id:
        return jsonify(message='forbidden', status=403), 403
    db.session.delete(g.user)
    db.session.commit()
    return jsonify({}), 204


@users_api.route('/api/users/<int:id>/votes')
@token_auth.login_required
def get_votes(id):
    """Get all votes of a user given his id."""
    if id != g.user.id:
        return jsonify(message='forbidden', status=403), 403
    votes = VoteSchema().dump(g.user.votes, many=True).data
    return jsonify(votes=votes), 200


@users_api.route('/api/users/<int:id>/favourites')
@token_auth.login_required
def get_favourites(id):
    """Get all bookmark favorites of a user given his id."""
    if id != g.user.id:
        return jsonify(message='forbidden', status=403), 403
    favs = FavouriteSchema().dump(g.user.favourites, many=True).data
    return jsonify(favourites=favs), 200
