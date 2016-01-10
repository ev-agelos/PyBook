"""Configuration module for the flask application."""


from os.path import dirname, abspath


class DefaultConfiguration:
    DATABASE = 'python_bookmarks.db'
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + dirname(abspath(__file__)) +
                               '/' + DATABASE)
    TESTING = False
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    RECORD_QUERIES = False
    SECRET_KEY = 'Basic_key_thats_supposed_to_be_secret'
    BCRYPT_LEVEL = 12
    USERNAME = 'admin'
    PASSWORD = 123
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(DefaultConfiguration):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True


class DebugConfig(DefaultConfiguration):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    RECORD_QUERIES = True
