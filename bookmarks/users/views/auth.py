"""Module to handle login/logout/register functions."""


from flask import (request, url_for, redirect, render_template, flash, g,
                   Blueprint)
from flask_login import login_user, logout_user, login_required

from bookmarks import db, utils

from ..forms import (LoginForm, RegistrationForm, RequestPasswordResetForm,
                     PasswordResetForm)
from ..models import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login to application."""
    if g.user and g.user.is_authenticated:
        flash('You are already signed in.', 'danger')
        return redirect('/')
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if not user:
            flash('Wrong credentials.', 'danger')
        else:
            if not user.active:
                flash('Email address is not verified yet.', 'info')
            elif not user.is_password_correct(form.password.data):
                flash('Wrong credentials.', 'danger')
            else:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                flash('Login was successful.', 'success')
                return redirect(url_for('bookmarks.get'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    g.user.authenticated = False
    db.session.commit()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)).first()
        if user and user.username == form.username.data and \
                user.email == form.email.data:
            flash('Username and email are already taken!')
        elif user and user.username == form.username.data:
            flash('Username is already taken!', 'warning')
        elif user and user.email == form.email.data:
            flash('Email is already taken!', 'warning')
        else:
            user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            user.auth_token = user.generate_auth_token()
            db.session.add(user)
            db.session.commit()
            activation_link = url_for('auth.confirm', token=user.auth_token,
                                      _external=True)
            text = ('Welcome {},\n\nactivate your account by clicking this'
                    ' link: {}'.format(user.username, activation_link))
            sent = utils.send_email('Account confirmation - PyBook',
                                    user.email, text)
            if sent:
                flash('A verification email has been sent to the registered '
                      'email address. Please follow the instructions to verify'
                      ' your email address.', 'info')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form)


@auth.route('/users/confirm/<token>')
def confirm(token):
    """Confirm a token."""
    data = User.verify_auth_token(token)
    user = User.query.get(data['id']) if data and data.get('id') else None
    if not data or 'id' not in data or user is None:
        flash('Confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index.home'))
    elif 'email' in data:
        same_email_user = User.query.filter_by(email=data['email']).scalar()
        if same_email_user is not None:
            flash('Confirmation link is invalid or has expired.', 'danger')
            return redirect(url_for('index.home'))
        user.email = data['email']
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        flash('Email updated successfully. You can now login with the new '
              'email address.', 'success')
    else:
        if user.active:
            flash('Your account is already activated, please login.', 'info')
        else:
            user.active = True
            db.session.add(user)
            db.session.commit()
            flash('Your account has been activated. You can now login.',
                  'success')
    return redirect(url_for('auth.login'))


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
            text = ('Hello {},\n\nSomeone, hopefully you, has requested to '
                    'reset the password for\nyour PyBook account on '
                    'https://pybook.evagelos.xyz.\nIf you did not perform this '
                    'request, you can safely ignore this email.\nOtherwise, '
                    'click the link below to complete the process.\n{}'
                    .format(user.username, activation_link))
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
        text = ('Hello {},\nThe password for your PyBook account on '
                'https://pybook.evagelos.xyz has successfully been changed.\nIf you '
                'did not initiate this change, please contact your \n'
                'administrator immediately.'.format(user.username))
        utils.send_email('Password changed', user.email, text)
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html', token=token, form=form)
