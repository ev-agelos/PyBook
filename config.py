"""Configuration module for the flask application."""


class DefaultConfiguration:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///python_bookmarks.db'
    DATABASE = 'python_bookmarks.db'
    TESTING = False
    DEBUG = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    RECORD_QUERIES = False
    SECRET_KEY = 'Basic_key_thats_supposed_to_be_secret'
    BCRYPT_LEVEL = 12
    USERNAME = 'admin'
    PASSWORD = 123


class TestConfig(DefaultConfiguration):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True


class DebugConfig(DefaultConfiguration):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    RECORD_QUERIES = True
