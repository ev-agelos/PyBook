"""Main module for the application."""

import os

from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import current_user, LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config=None):
    """Factory function to create the Flask application."""
    app = Flask(__name__, instance_relative_config=True, static_url_path='')

    bcrypt.init_app(app)
    login_manager = LoginManager(app)
    CsrfProtect(app)
    DebugToolbarExtension(app)

    if 'APP_CONFIG_FILE' in os.environ:
        app.config.from_envvar('APP_CONFIG_FILE')
    elif config is None:  # Use instance folder
        app.config.from_pyfile('development.py')
    else:
        app.config.from_object(config)
    # Database and mail should be initialized after config is decided
    db.init_app(app)
    mail.init_app(app)

    from bookmarks.views.bookmark_views import bookmarks, user_bookmarks
    bookmarks.BookmarksView.register(app)
    user_bookmarks.UsersView.register(app)

    from bookmarks.views.bookmark_views.bookmarks_crud import crud
    from main.views import index
    from bookmarks.views.helper_endpoints import helper_endpoints
    from auth.views import auth
    app.register_blueprint(crud)
    app.register_blueprint(index)
    app.register_blueprint(helper_endpoints)
    app.register_blueprint(auth)


    @app.before_request
    def before_request():
        """Save current user to g, to have him available in the entire session."""
        g.user = current_user


    from auth.models import User
    @login_manager.user_loader
    def user_loader(user_id):
        """Reload the user object from the user ID stored in the session."""
        return db.session.query(User).get(user_id)
    return app

