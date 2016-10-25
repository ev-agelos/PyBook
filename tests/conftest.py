"""Pytest fixtures for all tests to use."""

import os

import pytest
import requests

from bookmarks import create_app, db as _db
from bookmarks.users.models import User


@pytest.fixture(scope='session', autouse=True)
def app():
    """Return the flask application."""
    my_app = create_app('config.TestConfig')

    return my_app


@pytest.fixture(scope='session', autouse=True)
def db(app, request):
    """Session-wide test database."""
    # with app.app_context():
    _db.app = app
    _db.create_all()
    _db.session.commit()

    @request.addfinalizer
    def fin():
        """Close database after test finish."""
        os.close(app.config['DB_FD'])
        os.unlink(app.config['DATABASE'])

    return _db


@pytest.fixture
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    @request.addfinalizer
    def fin():
        transaction.rollback()
        connection.close()
        session.remove()

    return session


@pytest.fixture
def user(app, session, request):
    """Add a test user in the test database."""
    user = User(username='flask_user', email='flask@flask.com',
                password='123123', active=True)
    session.add(user)
    session.commit()
    with app.app_context():
        user.auth_token = user.generate_auth_token()
    session.add(user)
    session.commit()

    @request.addfinalizer
    def fin():
        """Delete user from database after test finishes."""
        session.delete(user)
        session.commit()

    return user


@pytest.fixture(autouse=True)
def patch_mail(monkeypatch):
    monkeypatch.setattr(requests, 'post', lambda *args, **kwargs: None)
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: None)
