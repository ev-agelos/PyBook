"""Configuration module for the flask application."""

from os.path import dirname, abspath
import tempfile


class CommonConfig:
    """Common configuration for all environments."""

    API_VERSION = '1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/api/v' + API_VERSION
    OPENAPI_SWAGGER_UI_PATH = '/documentation'
    OPENAPI_SWAGGER_UI_VERSION = '3.18.3'


class DevConfig(CommonConfig):
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
    RECAPTCHA_PUBLIC_KEY = ''
    TESTING = True
    RECAPTCHA_PRIVATE_KEY = ''


class TestConfig(DevConfig):
    """Testing configuration."""

    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SERVER_NAME = 'localhost.localdomain'
