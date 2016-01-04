"""Main module for the application."""

import os

from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import current_user
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy_wrapper import SQLAlchemy


app = Flask(__name__, instance_relative_config=True, static_url_path='')

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
csrf = CsrfProtect(app)
toolbar = DebugToolbarExtension(app)

app.config.from_object('config.DefaultConfiguration')
if 'APP_CONFIG_FILE' in os.environ:
    app.config.from_envvar('APP_CONFIG_FILE')


@app.before_request
def before_request():
    """Save current user to g, to have him available in the entire session."""
    g.user = current_user


db = SQLAlchemy(app.config['SQLALCHEMY_DATABASE_URI'], app=app,
                record_queries=app.config['RECORD_QUERIES'])


@login_manager.user_loader
def user_loader(user_id):
    """Reload the user object from the user ID stored in the session."""
    return db.query(User).get(user_id)

from bookmarks_app.models import User
from bookmarks_app.views import auth, index, helper_endpoints
from bookmarks_app.views.bookmark_views import (bookmarks, bookmarks_crud,
                                                user_bookmarks)

bookmarks.BookmarksView.register(app)
user_bookmarks.UsersView.register(app)
