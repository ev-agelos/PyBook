"""Module for creating the Forms for the application."""

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import InputRequired, email, url


class LoginForm(Form):

    """Login form for the application."""

    email = EmailField('email', validators=[InputRequired(), email()])
    password = PasswordField('password', validators=[InputRequired()])


class AddBookmark(Form):

    """Add bookmark form for the application."""

    category = StringField('category')
    title = StringField('title', validators=[InputRequired()])
    url = URLField('url', validators=[InputRequired(), url()])
