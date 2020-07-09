"""Forms for auth package."""


from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class ChangePasswordForm(FlaskForm):
    """Form for changing user's password."""

    password = PasswordField('Current password',
                             validators=[InputRequired(),
                                         Length(min=6, max=25)])
    new_password = PasswordField('New password',
                                 validators=[InputRequired(),
                                             Length(min=6, max=25)])
    confirm_password = PasswordField(
        'Confirm new password',
        validators=[InputRequired(),
                    EqualTo('new_password', message='Passwords must match.')])


class RequestPasswordResetForm(FlaskForm):
    """Form for requesting password reset."""

    email = StringField('Email', validators=[InputRequired(),
                                             Email(message=None),
                                             Length(min=6, max=40)])


class PasswordResetForm(FlaskForm):
    """Form for ressetting user's password."""

    new_password = PasswordField('New password',
                                 validators=[InputRequired(),
                                             Length(min=6, max=25)])
    confirm_password = PasswordField(
        'Confirm new password',
        validators=[InputRequired(),
                    EqualTo('new_password', message='Passwords must match.')])
