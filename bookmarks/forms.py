"""Module for creating the Forms for the application."""

from flask_wtf import Form
from wtforms import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, URL, Optional


class AddBookmarkForm(Form):
    """Add bookmark form for the application."""

    category = StringField('Category', default='uncategorized')
    title = StringField('Title', validators=[InputRequired()])
    url = URLField('Url', validators=[InputRequired(), URL()])


class UpdateBookmarkForm(Form):
    """Update a bookmark without requiring fields."""

    category = StringField('Category', default='uncategorized')
    title = StringField('Title')
    url = URLField('Url', validators=[Optional(), URL()])
