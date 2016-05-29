"""User endpoints."""

from flask import render_template, g, Blueprint, abort
from sqlalchemy.orm.exc import NoResultFound

from main import db

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
