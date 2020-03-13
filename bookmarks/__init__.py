"""Main module for the application."""

import os

from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import current_user, LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
csrf = CSRFProtect()
migrate = Migrate()

from .models import Tag, Bookmark, Vote, Favourite
from .users.models import User


def create_app():
    """Factory function to create the Flask application."""
    app = Flask(__name__, static_url_path='')
    bcrypt.init_app(app)
    login_manager = LoginManager(app)

    if app.env == 'production':
        app.config.from_envvar('APP_CONFIG_FILE')
        # Use Sentry service
        sentry_sdk.init(dsn=app.config['SENTRY_DSN'],
                        integrations=[FlaskIntegration()])
    elif app.env == 'development':
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_object('config.TestConfig')

    print(f"Loaded {app.env} configuration")

    # Database, CSRF should be attached after config is decided
    db.init_app(app)
    if app.env == 'development':
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
        migrate.init_app(app, db)

    with app.app_context():
        try:
            db.create_all()
        except OperationalError:
            pass  # database/tables already exist
    ma.init_app(app)
    csrf.init_app(app)

    # Regular views
    from bookmarks.views import index
    app.register_blueprint(index)
    from bookmarks.views.bookmarks import bookmarks
    from bookmarks.views.tags import tags
    from bookmarks.views.user_bookmarks import bookmarks_per_user
    from bookmarks.views.helper_endpoints import helper_endpoints
    from bookmarks.users.views.auth import auth
    from bookmarks.users.views.users import users
    for blueprint in (bookmarks, tags, bookmarks_per_user, helper_endpoints,
                      auth, users):
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

    @app.before_request
    def before_request():
        """Make logged in user available to Flask global variable g."""
        g.user = current_user

    @login_manager.user_loader
    def user_loader(user_id):
        """Reload the user object from the user ID stored in the session."""
        return db.session.query(User).get(user_id)

    return app
