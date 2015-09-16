"""Main module for the application."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__, instance_relative_config=True)
bcrypt = Bcrypt(app)

app.config.from_pyfile('development.py')

db = SQLAlchemy(app)
