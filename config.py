"""Configuration module for the flask application."""

import os
from os.path import dirname, abspath
import tempfile


class Common:
    """Common configuration for all environments."""

    API_VERSION = '1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/api/v' + API_VERSION
    OPENAPI_SWAGGER_UI_PATH = '/documentation'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    # Flask-SqlAlchemy event system is not being used
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Common):
    """Development configuration."""

    DATABASE = 'dev_pybook.db'
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + dirname(abspath(__file__)) +
                               '/' + DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    USERNAME = 'admin'
    PASSWORD = 123
    SECRET_KEY = 'key_thats_supposed_to_be_secret'
    BCRYPT_LEVEL = 12
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    TESTING = True
    RECAPTCHA_PRIVATE_KEY = ''
    CELERY_BROKER_URL='amqp://localhost:5672'


class Testing(Development):
    """Testing configuration."""

    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SERVER_NAME = 'localhost.localdomain'


class Production(Common):

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # get values from environment only in production
    # otherwise they will not exist
    if 'FLASK_ENV' not in os.environ or os.environ['FLASK_ENV'] == 'production':
        SECRET_KEY = os.environ['SECRET_KEY']
        BCRYPT_LEVEL = os.environ['BCRYPT_LEVEL']
        DATABASE = os.environ['DATABASE']
        SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
        USERNAME = os.environ['USERNAME']
        PASSWORD = os.environ['PASSWORD']
        MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']
        SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
        RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']
        SENTRY_DSN = os.environ['SENTRY_DSN']
        CLOUDINARY_CLOUD_NAME = os.environ['CLOUDINARY_CLOUD_NAME']
        CLOUDINARY_API_KEY = os.environ['CLOUDINARY_API_KEY']
        CLOUDINARY_SECRET_KEY = os.environ['CLOUDINARY_SECRET_KEY']
        CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
