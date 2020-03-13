"""Configuration module for the flask application."""


import os
from os.path import dirname, abspath
import tempfile


class DevConfig:
    """Development configuration."""

    DATABASE = 'dev_pybook.db'
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + dirname(abspath(__file__)) +
                               '/' + DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    USERNAME = 'admin'
    PASSWORD = 123
    TESTING = False
    SECRET_KEY = 'key_thats_supposed_to_be_secret'
    BCRYPT_LEVEL = 12
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestConfig(DevConfig):
    """Testing configuration."""

    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    TESTING = True
    SERVER_NAME = 'localhost.localdomain'
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''
