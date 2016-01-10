"""Pytest fixtures for all tests to use."""

import os
import tempfile

import pytest

from bookmarks_app import create_app, db


@pytest.fixture
def app(request):
    """Return the flask application."""
    my_app = create_app('config.TestConfig')

    db_fd, my_app.config['DATABASE'] = tempfile.mkstemp()
    my_app.config['SQLALCHEMY_DATABASE_URI'] += '/' + my_app.config['DATABASE']
    application = my_app.test_client()
    with my_app.app_context():
        db.create_all()
        db.session.commit()

    def fin():
        """Close database after test finish."""
        os.close(db_fd)
        os.unlink(my_app.config['DATABASE'])
    request.addfinalizer(fin)
    return application
