"""User endpoints."""

from flask import render_template, g, Blueprint, abort

from bookmarks import db

from ..models import User
from ..forms import ProfileForm, ChangePasswordForm

users = Blueprint('users', __name__)


@users.route('/users/')
@users.route('/users/<int:id>')
def get_users(id=None):
    """Return all users or the user with the given <id>."""
    if id is None:
        users = db.session.query(User).all()
        return render_template('auth/list_users.html', users=users)

    if g.user.is_authenticated and id == g.user.id:
        user = g.user
        form = ProfileForm(obj=g.user)
    else:
        user = User.query.get(id)
        if user is None:
            abort(404)
        form = ProfileForm(formdata=None)
    password_form = ChangePasswordForm()
    return render_template('auth/profile.html', user=user, profile_form=form,
                           password_form=password_form)
