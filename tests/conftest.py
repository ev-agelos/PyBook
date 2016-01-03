"""Pytest fixtures for all tests to use."""

import os
import tempfile

import pytest
from sqlalchemy_wrapper import SQLAlchemy

from bookmarks_app import app as my_app


SETTINGS = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite://:memory',
    'TESTING': True,
    'DEBUG': False,
    'DEBUG_TB_INTERCEPT_REDIRECTS': False,
    'RECORD_QUERIES': False,
    'SECRET_KEY': 'testing',
    'BCRYPT_LEVEL': 12,
    'USERNAME': 'admin',
    'PASSWORD': 123}


@pytest.fixture
def app(request):
    """Return the flask application."""
    db_fd, my_app.config['DATABASE'] = tempfile.mkstemp()
    my_app.config['SQLALCHEMY_DATABASE_URI'] += my_app.config['DATABASE']
    application = my_app.test_client()

    my_app.config.update(SETTINGS)
    with my_app.app_context():
        database = SQLAlchemy(my_app.config['SQLALCHEMY_DATABASE_URI'],
                              app=my_app,
                              record_queries=my_app.config['RECORD_QUERIES'])
        database.create_all()
        database.commit()

    def fin():
        """Close database after test finish."""
        os.close(db_fd)
        os.unlink(my_app.config['DATABASE'])
    request.addfinalizer(fin)
    return application
