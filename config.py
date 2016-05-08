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
    RECORD_QUERIES = False
    SECRET_KEY = 'Basic_key_thats_supposed_to_be_secret'
    BCRYPT_LEVEL = 12

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_DEFAULT_SENDER = ''
    MAIL_PASSWORD = ''


class TestConfig(DefaultConfiguration):
    """Configuration for tests."""

    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    TESTING = True
