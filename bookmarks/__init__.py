"""Main module for the application."""

import os

from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import current_user, LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask_recaptcha import ReCaptcha
from flask_marshmallow import Marshmallow
from raven.contrib.flask import Sentry


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
csrf = CsrfProtect()
re_captcha = ReCaptcha()
sentry = Sentry()

from .models import Category, Bookmark, Vote, Favourite
from .users.models import User


def create_app(config=None):
    """Factory function to create the Flask application."""
    app = Flask(__name__, static_url_path='')
    bcrypt.init_app(app)
    login_manager = LoginManager(app)

    # Production
    if 'APP_CONFIG_FILE' in os.environ:
        app.config.from_envvar('APP_CONFIG_FILE')
        # Use OpBeat service
        from opbeat.contrib.flask import Opbeat
        opbeat = Opbeat(app,
                        organization_id=app.config['OPBEAT_ORGANIZATION_ID'],
                        app_id=app.config['OPBEAT_APP_ID'],
                        secret_token=app.config['OPBEAT_SECRET_TOKEN'])
        # Use Sentry service
        sentry.dns = app.config['SENTRY_DSN']
        sentry.init_app(app)
    # Development/Testing
    else:
        app.config.from_object(config)
        print('Loaded {} configuration'.format(config))
        if app.config['DEBUG']:
            from flask_debugtoolbar import DebugToolbarExtension
            DebugToolbarExtension(app)

    # Database, CSRF, reCaptcha should be attached after config is decided
    re_captcha.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    ma.init_app(app)
    csrf.init_app(app)

    # Regular views
    from bookmarks.views import index
    app.register_blueprint(index)
    from bookmarks.views.bookmarks import bookmarks
    from bookmarks.views.categories import categories
    from bookmarks.views.bookmarks_crud import crud
    from bookmarks.views.user_bookmarks import bookmarks_per_user
    from bookmarks.views.helper_endpoints import helper_endpoints
    from bookmarks.users.views.auth import auth
    from bookmarks.users.views.users import users
    for blueprint in (bookmarks, categories, crud, bookmarks_per_user,
                      helper_endpoints, auth, users):
        app.register_blueprint(blueprint)

    # API endpoints
    from bookmarks.api.users import users_api
    app.register_blueprint(users_api)
    from bookmarks.api.auth import auth_api
    app.register_blueprint(auth_api)
    from bookmarks.api.bookmarks import bookmarks_api
    app.register_blueprint(bookmarks_api)
    from bookmarks.api.votes import votes_api
    app.register_blueprint(votes_api)
    from bookmarks.api.favourites import favourites_api
    app.register_blueprint(favourites_api)

    @app.before_request
    def before_request():
        """Make logged in user available to Flask global variable g."""
        g.user = current_user

    @login_manager.user_loader
    def user_loader(user_id):
        """Reload the user object from the user ID stored in the session."""
        return db.session.query(User).get(user_id)

    return app
