"""Main module for the application."""

from flask import Flask, g
from sqlalchemy_wrapper import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import current_user, LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__, instance_relative_config=True, static_url_path='')

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
csrf = CsrfProtect(app)
toolbar = DebugToolbarExtension(app)

app.config.from_pyfile('development.py')

db = SQLAlchemy(app.config['SQLALCHEMY_DATABASE_URI'], app=app,
                record_queries=app.config['RECORD_QUERIES'])


@app.before_request
def before_request():
    """Save current user to g, to have him available in the entire session."""
    g.user = current_user


from bookmarks_app.models import User
from bookmarks_app.views import auth, index
from bookmarks_app.views.bookmark_views import (bookmarks, bookmarks_crud,
                                                user_bookmarks)
from bookmarks_app.views.helper_endpoints import suggest_title
bookmarks.BookmarksView.register(app)
user_bookmarks.UsersView.register(app)


@login_manager.user_loader
def user_loader(user_id):
    """Reload the user object from the user ID stored in the session."""
    return db.query(User).get(user_id)
