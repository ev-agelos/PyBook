"""Pytest fixtures for all tests to use."""

import os
import tempfile

import pytest
from sqlalchemy_wrapper import SQLAlchemy

from bookmarks_app import app as my_app


@pytest.fixture
def app(request):
    """Return the flask application."""
    db_fd, my_app.config['DATABASE'] = tempfile.mkstemp()
    application = my_app.test_client()

    my_app.config.from_pyfile('testing.py')
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
