"""Module for creating the Forms for the application."""

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextField, BooleanField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import InputRequired, Email, URL, EqualTo, Length


class LoginForm(Form):

    """Login form for the application."""

    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')


class AddBookmarkForm(Form):

    """Add bookmark form for the application."""

    category = StringField('category')
    title = StringField('title', validators=[InputRequired()])
    url = URLField('url', validators=[InputRequired(), URL()])


class RegistrationForm(Form):

    """Registration form for new users."""

    username = TextField(
        'username', validators=[InputRequired(), Length(min=3, max=25)])
    email = TextField(
        'email', validators=[InputRequired(), Email(message=None),
                             Length(min=6, max=40)])
    password = PasswordField(
        'password', validators=[InputRequired(), Length(min=6, max=25)])
    confirm_password = PasswordField(
        'Repeat password',
        validators=[InputRequired(), EqualTo('password',
                                             message='Passwords must match.')])
