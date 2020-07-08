"""This module contains the landing endpoint."""

from flask import Blueprint, render_template

from bookmarks import db

index = Blueprint('index', __name__)


@index.route('/')
def home():
    """Landing page."""
    return render_template('index.html')
