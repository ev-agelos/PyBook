"""Main module for the application."""

from flask import Flask, g
from sqlalchemy_wrapper import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import current_user


app = Flask(__name__, instance_relative_config=True, static_url_path='')
bcrypt = Bcrypt(app)

app.config.from_pyfile('development.py')

db = SQLAlchemy(app.config['SQLALCHEMY_DATABASE_URI'], app=app,
                record_queries=app.config['RECORD_QUERIES'])


@app.before_request
def before_request():
    """Save current user to g, to have him available in the entire session."""
    g.user = current_user
