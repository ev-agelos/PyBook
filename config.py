"""Configuration module for the flask application."""


import os
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
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'Basic_key_thats_supposed_to_be_secret'
    BCRYPT_LEVEL = 12


class DevConfig(DefaultConfiguration):
    """Configuration for development."""

    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True

    MAILGUN_SENDER = os.environ['MAILGUN_SENDER']
    MAILGUN_KEY = os.environ['MAILGUN_KEY']
    MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']

    RECAPTCHA_SITE_KEY = os.environ['RECAPTCHA_SITE_KEY']
    RECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']


class TestConfig(DefaultConfiguration):
    """Configuration for tests."""

    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    TESTING = True
