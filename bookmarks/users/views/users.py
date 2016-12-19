"""User endpoints."""

from flask import render_template, g, Blueprint, abort, jsonify
from flask_login import login_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from bookmarks import db, csrf

from ..models import User

users = Blueprint('users', __name__)


@users.route('/users')
def get_users():
    """Return all users."""
    users = db.session.query(User).all()
    return render_template('auth/list_users.html', users=users)


@users.route('/users/<username>')
def get_user(username=''):
    """Return all users."""
    if username:
        try:
            if g.user.is_authenticated and username == g.user.username:
                user = g.user
            else:
                user = db.session.query(User).filter_by(
                    username=username).one()
        except NoResultFound:
            abort(404)
        return render_template('auth/profile.html', user=user)
    else:
        abort(404)


@users.route('/users/<int:id>/subscribe', methods=['POST'])
@csrf.exempt
@login_required
def subscribe(id):
    """Subscribe to a user."""
    if id == g.user.id:
        raise BadRequest
    user = User.query.get(id)
    if user is None:
        abort(404)
    subscription = g.user.subscribe(user)
    if subscription is None:
        raise BadRequest
    db.session.add(subscription)
    db.session.commit()
    response = jsonify({})
    response.status_code = 201
    return response


@users.route('/users/<int:id>/unsubscribe', methods=['DELETE'])
@csrf.exempt
@login_required
def unsubscribe(id):
    """Unsubscribe from a user."""
    if id == g.user.id:
        raise BadRequest
    user = User.query.get(id)
    if user is None:
        abort(404)
    subscription = g.user.unsubscribe(user)
    if subscription is None:
        raise BadRequest
    db.session.add(subscription)
    db.session.commit()
    return jsonify({}), 204
