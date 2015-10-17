"""User endpoint views."""

from flask import render_template, abort
from sqlalchemy.orm.exc import NoResultFound

from bookmarks import app, db
from bookmarks.models import User


@app.route('/users/')
@app.route('/users/<username>')
def get_users(username=''):
    """Return all users."""
    if username:
        try:
            user = db.session.query(User).filter_by(username=username).one()
        except NoResultFound:
            abort(404)
        return render_template('profile.html', user=user)
    else:
        users = db.session.query(User).all()
        return render_template('list_users.html', users=users)
