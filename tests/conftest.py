"""Pytest fixtures for all tests to use."""

import os

import pytest

from bookmarks import create_app, db as db_
from bookmarks.users.models import User


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    """Return the flask application."""
    app_ = create_app('config.TestConfig')

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


@pytest.yield_fixture
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


@pytest.yield_fixture
def user(app, session, request):
    """Add a test user in the test database."""
    user_ = User(username='flask_user', email='flask@flask.com',
                 password='123123', active=True)
    session.add(user_)
    session.commit()
    with app.app_context():
        user_.auth_token = user_.generate_auth_token()
    session.add(user_)
    session.commit()
    yield user_

    session.delete(user_)
    session.commit()


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
