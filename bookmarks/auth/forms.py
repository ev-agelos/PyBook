"""Forms for auth package."""


from flask_wtf import Form
from wtforms import PasswordField, TextField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class LoginForm(Form):
    """Login form for the application."""

    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')


class RegistrationForm(Form):
    """Registration form for new users."""

    username = TextField('Username', validators=[InputRequired(),
                                                 Length(min=3, max=25)])
    email = TextField('Email', validators=[InputRequired(),
                                           Email(message=None),
                                           Length(min=6, max=40)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=6, max=25)])
    confirm_password = PasswordField(
        'Repeat password',
        validators=[InputRequired(), EqualTo('password',
                                             message='Passwords must match.')])
