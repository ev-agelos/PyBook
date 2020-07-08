"""Module to handle login/logout/register functions."""


from flask import (request, url_for, redirect, render_template, flash,
                   Blueprint)

from bookmarks import db, utils

from ..forms import (LoginForm, RegistrationForm, RequestPasswordResetForm,
                     PasswordResetForm)
from ..models import User


auth = Blueprint('auth', __name__)


@auth.route('/users/password/request-reset', methods=['GET', 'POST'])
def request_password_reset():
    """Request to reset user's password."""
    form = RequestPasswordResetForm()
    if request.method == 'GET':
        return render_template('auth/request_password_reset.html', form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).scalar()
        if user is not None:
            user.auth_token = user.generate_auth_token()
            activation_link = url_for('auth.reset_password',
                                      token=user.auth_token, _external=True)
            text = (
                'Hello {},\n\nSomeone, hopefully you, has requested to reset '
                'the password for\nyour PyBook account on {}.\nIf you did not '
                'perform this request, you can safely ignore this email.\n'
                'Otherwise, click the link below to complete the process.\n{}'
            ).format(user.username, request.host_url,
                     activation_link)
            utils.send_email('Reset password instructions', user.email, text)
            db.session.add(user)
            db.session.commit()
    flash('If your email address exists in our database, you will receive a '
          'password recovery link at your email address.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/users/password/reset', methods=['GET', 'POST'])
def reset_password():
    """Reset user's password."""
    token = request.args.get('token', '')
    data = User.verify_auth_token(token)
    user = User.query.get(data['id']) if data and data.get('id') else None
    if not all([data, user]):
        flash('Your password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.request_password_reset'))
    if request.method == 'GET':
        form = PasswordResetForm()
        return render_template('auth/password_reset.html', token=token,
                               form=form)
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password = form.new_password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been changed successfully.', 'success')
        text = (
            'Hello {},\nThe password for your PyBook account on {} has '
            'successfully been changed.\nIf you did not initiate this change, '
            'please contact your \nadministrator immediately.'
        ).format(user.username, request.host_url)
        utils.send_email('Password changed', user.email, text)
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html', token=token, form=form)
