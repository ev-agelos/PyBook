from flask import g, jsonify, url_for, request
from flask.views import MethodView

from bookmarks import db, csrf
from bookmarks.users.models import User, SubscriptionsSchema

from .auth import token_auth


class SubscriptionsAPI(MethodView):

    decorators = [csrf.exempt, token_auth.login_required]

    def get(self):
        """Return subscriptions for a given user id."""
        # FIXME improve the boolean
        if request.args.get('mySubscribers') == 'true':
            subscribers = SubscriptionsSchema().dump(g.user.subscribers.all(), many=True)
            return jsonify(subscribers=subscribers), 200

        subscribed = SubscriptionsSchema().dump(g.user.subscribed.all(), many=True)
        return jsonify(subscriptions=subscribed), 200

    def post(self):
        """Subscribe to a user."""
        payload = request.get_json() or {}
        user_id = payload.get('user_id')
        if user_id is None:
            return jsonify(message='bad data', status=400), 400

        if user_id == g.user.id:
            return jsonify(message='Cannot subscribe to yourself', status=400), 400
        user = User.query.get(user_id)
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
        response.headers['Location'] = url_for(
            'subscriptions_api',
            _external=True
        )
        return response

    def delete(self, id):
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
        db.session.add(subscription)
        db.session.commit()
        return jsonify({}), 204


subscriptions_api = SubscriptionsAPI.as_view('subscriptions_api')
