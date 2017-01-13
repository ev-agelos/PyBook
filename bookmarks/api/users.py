"""API endpoints for users."""


from flask import g, jsonify, Blueprint, url_for

from bookmarks import db, csrf
from bookmarks.models import FavouriteSchema, VoteSchema, Vote
from bookmarks.users.models import (User, UserSchema, subscriptions,
                                    SubscriptionsSchema)

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
            return jsonify(message='User not found', status=404), 404
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
    """Delete an existing user and his favourites."""
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
    votes = VoteSchema().dump(g.user.votes.all(), many=True).data
    return jsonify(votes=votes), 200


@users_api.route('/api/users/<int:id>/favourites')
@token_auth.login_required
def get_favourites(id):
    """Get all bookmark favorites of a user given his id."""
    if id != g.user.id:
        return jsonify(message='forbidden', status=403), 403
    favs = FavouriteSchema().dump(g.user.favourites.all(), many=True).data
    return jsonify(favourites=favs), 200


@users_api.route('/api/users/<int:id>/subscribers')
@token_auth.login_required
def get_subscribers(id):
    """Return user's subscribers."""
    user = User.query.get(id)
    if user is None:
        return jsonify(message='User not found', status=404), 404
    subscribers = SubscriptionsSchema().dump(user.subscribers.all(), many=True).data
    return jsonify(subscribers=subscribers), 200


@users_api.route('/api/users/<int:id>/subscriptions')
@token_auth.login_required
def get_subscriptions(id):
    """Return user's subscriptions."""
    user = User.query.get(id)
    if user is None:
        return jsonify(message='User not found', status=404), 404
    subscribed = SubscriptionsSchema().dump(user.subscribed, many=True).data
    return jsonify(subscriptions=subscribed), 200


@users_api.route('/api/users/<int:id>/subscribe', methods=['POST'])
@token_auth.login_required
@csrf.exempt
def subscribe(id):
    """Subscribe to a user."""
    if id == g.user.id:
        return jsonify(message='Cannot subscribe to yourself', status=400), 400
    user = User.query.get(id)
    if user is None:
        return jsonify(message='User not found', status=404), 404
    subscription = g.user.subscribe(user)
    if subscription is None:
        return jsonify(message='You are already subscribed to ' + user.username,
                       status=409), 409
    db.session.add(subscription)
    db.session.commit()
    response = jsonify({})
    response.status_code = 201
    response.headers['Location'] = url_for('users_api.get_subscribers',
                                           id=user.id, subscriber_id=g.user.id,
                                           _external=True)
    return response


@users_api.route('/api/users/<int:id>/unsubscribe', methods=['DELETE'])
@token_auth.login_required
@csrf.exempt
def unsubscribe(id):
    """Un-subscribe from a user."""
    if id == g.user.id:
        return jsonify(message='Cannot unsubscribe from yourself',
                       status=400), 400
    user = User.query.get(id)
    if user is None:
        return jsonify(message='User not found', status=404), 404
    subscription = g.user.unsubscribe(user)
    if subscription is None:
        return jsonify(message='You are not subscribed to ' + user.username,
                       status=409), 409
    # TODO add or delete here?
    db.session.add(subscription)
    db.session.commit()
    return jsonify({}), 204
