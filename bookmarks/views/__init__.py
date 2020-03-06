"""This module contains the landing endpoint."""

from flask import Blueprint, redirect, url_for

from bookmarks import db

index = Blueprint('index', __name__)


@index.route('/')
def home():
    """Landing page."""
    return redirect(url_for('bookmarks.get'))
