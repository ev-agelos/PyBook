"""Pytest fixtures for all tests to use."""

import os

import pytest

from bookmarks import create_app, db as db_
from bookmarks.users.models import User


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    """Return the flask application."""
    os.environ['FLASK_ENV'] = 'testing'
    app_ = create_app()

    ctx = app_.app_context()
    ctx.push()
    yield app_

    ctx.pop()


@pytest.yield_fixture(scope='session', autouse=True)
def db(app):
    """Session-wide test database."""
    db_.app = app
    db_.create_all()
    yield db_

    db_.drop_all()
    os.close(app.config['DB_FD'])
    os.unlink(app.config['DATABASE'])


class _dict(dict):
    def __nonzero__(self):
        return True


@pytest.yield_fixture(autouse=True)
def session(app, db, monkeypatch):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    # Next line made all work, taken from:
    # https://github.com/mitsuhiko/flask-sqlalchemy/pull/249
    # Patch Flask-SQLAlchemy to use our connection
    monkeypatch.setattr(db, 'get_engine', lambda *args: connection)

    # had to create a subclass of dict to pass to binds, look here:
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/345
    # probably in flask-sqlalchemy version 3(next one) this gets fixed
    options = dict(bind=connection, binds=_dict())
    session_ = db.create_scoped_session(options=options)
    db.session = session_
    yield session_
    transaction.rollback()
    connection.close()
    session_.remove()


@pytest.fixture
def user(app, session, request):
    """Add a test user in the test database."""
    user_ = User(id=1, username='flask_user', email='flask@flask.com',
                 password='123123', active=True)
    user_.auth_token = user_.generate_auth_token()
    session.add(user_)
    session.commit()
    return user_


@pytest.fixture(autouse=True)
def patch_mail(monkeypatch):
    """Return True always when invoking the send_email function."""
    monkeypatch.setattr('bookmarks.utils.send_email', lambda *args: True)


@pytest.fixture(autouse=True)
def patch_get_thumbnail(monkeypatch):
    """Return None as the thumbnail couldn't be downloaded."""
    monkeypatch.setattr('bookmarks.views.utils.get_url_thumbnail',
                        lambda *args: None)


@pytest.fixture(autouse=True)
def patch_requests_library(monkeypatch):
    """Return True when make calls with requests library."""
    monkeypatch.setattr('requests.get', lambda *args, **kwargs: True)
    monkeypatch.setattr('requests.post', lambda *args, **kwargs: True)


@pytest.fixture
def api(app, user):
    """Helper client with the advantage of using the corrent API path."""

    class APIClient:

        path = f"/api/v{app.config['API_VERSION']}"

        def __init__(self):
            self.client = app.test_client()

        def _set_headers(self, kwargs):
            """Set headers respecting if ones were passed."""
            kwargs['content_type'] = 'application/json'
            if not 'headers' in kwargs:
                kwargs['headers'] = {}

            headers = {'Authorization': f'Bearer {user.auth_token}'}
            for key, value in headers.items():
                if key not in kwargs['headers']:
                    kwargs['headers'][key] = value

        def get(self, path, **kwargs):
            self._set_headers(kwargs)
            return self.client.get(APIClient.path + path, **kwargs)

        def post(self, path, **kwargs):
            self._set_headers(kwargs)
            return self.client.post(APIClient.path + path, **kwargs)

        def put(self, path, **kwargs):
            self._set_headers(kwargs)
            return self.client.put(APIClient.path + path, **kwargs)

        def delete(self, path, **kwargs):
            self._set_headers(kwargs)
            return self.client.delete(APIClient.path + path, **kwargs)

    return APIClient()
