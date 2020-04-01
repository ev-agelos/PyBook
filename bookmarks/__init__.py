"""Main module for the application."""

import os

from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import current_user, LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_marshmallow import Marshmallow
from flask_smorest import Api
from flask_migrate import Migrate
from celery import Celery
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
csrf = CSRFProtect()
migrate = Migrate()
smorest_api = Api()

if os.environ.get('FLASK_ENV') == 'development':
    import config
    celery = Celery(__name__, broker=config.Development.CELERY_BROKER_URL)
elif os.environ.get('FLASK_ENV') == 'testing':
    pass
else:
    celery = Celery(__name__, broker=os.environ.get('CELERY_BROKER_URL'))

from .users.models import User


def create_app():
    """Factory function to create the Flask application."""
    app = Flask(__name__, static_url_path='')
    bcrypt.init_app(app)
    login_manager = LoginManager(app)

    app.config.from_object(f'config.{app.env.title()}')
    if app.env == 'production':
        celery.conf.update(app.config)
        if celery.conf.broker_url != app.config['CELERY_BROKER_URL']:
            raise RuntimeError("Celery url is different from app's configuration")
        # Use Sentry service
        sentry_sdk.init(dsn=app.config['SENTRY_DSN'],
                        integrations=[FlaskIntegration()])
    elif app.env == 'development':
        celery.conf.update(app.config)
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    # Database, CSRF should be attached after config is decided
    db.init_app(app)
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
    app.add_url_rule(
        '/api/v1/users/',
        view_func=users_api,
        defaults={'id': None},
        methods=['GET']
    )
    app.add_url_rule(
        '/api/v1/users/<int:id>',
        view_func=users_api,
        methods=['GET', 'PUT', 'DELETE']
    )

    from bookmarks.api.subscriptions import subscriptions_api
    app.add_url_rule(
        '/api/v1/subscriptions',
        view_func=subscriptions_api,
        methods=['GET']
    )
    app.add_url_rule(
        '/api/v1/subscriptions',
        view_func=subscriptions_api,
        methods=['POST']
    )
    app.add_url_rule(
        '/api/v1/subscriptions/<int:id>',
        view_func=subscriptions_api,
        methods=['DELETE']
    )

    from bookmarks.api.auth import auth_api
    app.register_blueprint(auth_api)

    smorest_api.init_app(app)
    from bookmarks.api.bookmarks import bookmarks_api
    smorest_api.register_blueprint(bookmarks_api)

    from bookmarks.api.favourites import favourites_api
    app.add_url_rule(
        '/api/v1/favourites/',
        view_func=favourites_api,
        defaults={'id': None},
        methods=['GET']
    )
    app.add_url_rule(
        '/api/v1/favourites/',
        view_func=favourites_api,
        methods=['POST']
    )
    app.add_url_rule(
        '/api/v1/favourites/<int:id>',
        view_func=favourites_api,
        methods=['GET', 'DELETE']
    )

    from bookmarks.api.votes import votes_api
    app.add_url_rule(
        '/api/v1/votes/',
        view_func=votes_api,
        defaults={'id': None},
        methods=['GET']
    )
    app.add_url_rule(
        '/api/v1/votes/<int:id>',
        view_func=votes_api,
        methods=['GET', 'PUT', 'DELETE']
    )
    app.add_url_rule(
        '/api/v1/votes/',
        view_func=votes_api,
        methods=['POST']
    )

    @app.before_request
    def before_request():
        """Make logged in user available to Flask global variable g."""
        g.user = current_user

    @login_manager.user_loader
    def user_loader(user_id):
        """Reload the user object from the user ID stored in the session."""
        return db.session.query(User).get(user_id)

    return app
