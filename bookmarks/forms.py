"""Module for creating the Forms for the application."""

from flask_wtf import FlaskForm
from wtforms import StringField, FieldList
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, URL, Optional, DataRequired


class AddBookmarkForm(FlaskForm):
    """Add bookmark form for the application."""

    title = StringField('Title', validators=[InputRequired()])
    url = URLField('Url', validators=[InputRequired(), URL()])
    tags = FieldList(StringField(filters=[lambda x: x or 'uncategorized']))


class UpdateBookmarkForm(FlaskForm):
    """Update a bookmark without requiring fields."""

    title = StringField('Title')
    url = URLField('Url', validators=[Optional(), URL()])
    tags = FieldList(StringField(filters=[lambda x: x or 'uncategorized']))
