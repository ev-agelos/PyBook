from flask import g
from flask.views import MethodView
from flask_login import login_required
from flask_smorest import Blueprint, abort

from bookmarks import db, csrf
from bookmarks.users.models import User
from .schemas import SubscriptionsSchema, SubscriptionsGETSchema, SubscriptionsPOSTSchema


subscriptions_api = Blueprint('subscriptions_api', 'Subscriptions', url_prefix='/api/v1/subscriptions/',
                              description='Operations on Subscriptions')


@subscriptions_api.route('/')
class SubscriptionsAPI(MethodView):

    decorators = [csrf.exempt, login_required]

    @subscriptions_api.arguments(SubscriptionsGETSchema, location='query')
    @subscriptions_api.response(SubscriptionsSchema(many=True))
    def get(self, args):
        """Return subscriptions for a given user id."""
        if args['mySubscribers'] is True:
            return g.user.subscribers.all()
        return g.user.subscribed.all()

    @subscriptions_api.arguments(SubscriptionsPOSTSchema)
    @subscriptions_api.response(code=204)
    def post(self, data):
        """Subscribe to a user."""
        if data['user_id'] == g.user.id:
            abort(409, message='Cannot subscribe to yourself')
        user = User.query.get(data['user_id'])
        if not user:
            abort(409, message='User not found')
        subscription = g.user.subscribe(user)
        if not subscription:
            abort(409, message='Subscription already exists')
        db.session.add(subscription)
        db.session.commit()


@subscriptions_api.route('/<int:id>')
class SubscriptionAPI(MethodView):

    decorators = [csrf.exempt, login_required]

    @subscriptions_api.response(code=204)
    def delete(self, id):
        """Un-subscribe from a user."""
        if id == g.user.id:
            abort(409, message='Cannot unsubscribe from yourself')
        user = User.query.get(id)
        if not user or not g.user.is_subscribed_to(user):
            abort(409, message='Subscription not found')
        g.user.unsubscribe(user)
        db.session.add(g.user)
        db.session.commit()
