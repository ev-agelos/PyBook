"""Configuration module for the flask application."""


from os.path import dirname, abspath, join


_cwd = dirname(abspath(__file__))
_db_dir = _cwd.replace('instance', '')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_db_dir, 'python_bookmarks.db')
DATABASE = 'python_bookmarks.db'
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
RECORD_QUERIES = True
SECRET_KEY = 'development'
BCRYPT_LEVEL = 12
USERNAME = 'admin'
PASSWORD = 123
