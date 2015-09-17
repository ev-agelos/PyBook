"""User endpoint views."""

from flask import render_template, abort

from bookmarks import app
from bookmarks.models import User


@app.route('/users/')
@app.route('/users/<int:user_id>')
def get_users(user_id=None):
    """Return all users."""
    if user_id is not None:
        user = User.query.get(user_id)
        if not user:
            abort(404)
        return render_template('profile.html', user=user)
    else:
        users = User.query.all()
        return render_template('list_users.html', users=users)
