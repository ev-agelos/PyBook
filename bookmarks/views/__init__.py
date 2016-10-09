"""This module contains the landing endpoint."""

from flask import request, Blueprint, render_template
from sqlalchemy.sql.expression import asc, desc

from bookmarks import db
from bookmarks.models import Bookmark
from bookmarks.auth.forms import RegistrationForm
from .utils import custom_render


index = Blueprint('index', __name__)


@index.route('/')
def home():
    """Landing page."""
    form = RegistrationForm()
    return render_template('index.html', form=form)
