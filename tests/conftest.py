"""Pytest fixtures for all tests to use."""

import os
import tempfile

import pytest
from sqlalchemy_wrapper import SQLAlchemy

import bookmarks_app as my_app


@pytest.fixture
def app(request):
    """Return the flask application."""
    my_app.app.config.from_object('config.TestConfig')

    db_fd, my_app.app.config['DATABASE'] = tempfile.mkstemp()
    my_app.app.config['SQLALCHEMY_DATABASE_URI'] += \
        '/' + my_app.app.config['DATABASE']
    application = my_app.app.test_client()

    with my_app.app.app_context():
        my_app.db = SQLAlchemy(my_app.app.config['SQLALCHEMY_DATABASE_URI'],
                               app=my_app.app)
        my_app.db.create_all()
        my_app.db.commit()

    def fin():
        """Close database after test finish."""
        os.close(db_fd)
        os.unlink(my_app.app.config['DATABASE'])
    request.addfinalizer(fin)
    return application
