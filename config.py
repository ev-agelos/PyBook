"""Configuration module for the flask application."""


from os.path import dirname, abspath
import tempfile


class DefaultConfiguration:
    """Default configuration."""

    DATABASE = 'python_bookmarks.db'
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + dirname(abspath(__file__)) +
                               '/' + DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    USERNAME = 'admin'
    PASSWORD = 123
    TESTING = False
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = 'Basic_key_thats_supposed_to_be_secret'
    BCRYPT_LEVEL = 12

    MAILGUN_SENDER = 'pybookmarks@mailgun.org'
    MAILGUN_KEY = ''
    MAILGUN_DOMAIN = ''


class TestConfig(DefaultConfiguration):
    """Configuration for tests."""

    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    TESTING = True
