"""Module to handle login/logout/register functions."""


from flask import (request, url_for, redirect, render_template, flash, g,
                   Blueprint, current_app)
from flask_login import login_user, logout_user, login_required
import requests
from sqlalchemy.orm.exc import NoResultFound

from bookmarks import db, re_captcha

from ..forms import LoginForm, RegistrationForm
from ..models import User
from .. import token as token_


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login to application."""
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
                return redirect(url_for('BookmarksView:index'))
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
    if form.validate_on_submit() and re_captcha.verify():
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
            token = token_.generate(form.email.data,
                                   current_app.config['SECRET_KEY'])
            user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data, email_token=token)
            db.session.add(user)
            db.session.commit()
            activation_link = url_for('auth.activate', token=token,
                                      _external=True)
            payload = {
                'subject': 'Account confirmation - Python Bookmarks',
                'text': 'Welcome {},\n\nactivate your account by clicking this'
                        ' link: {}'.format(user.username, activation_link),
                'to': [user.email],
                'from': current_app.config['MAILGUN_SENDER']}
            requests.post(current_app.config['MAILGUN_DOMAIN'],
                          auth=('api', current_app.config['MAILGUN_KEY']),
                          data=payload)
            flash('A verification email has been sent to the registered email '
                  'address. Please follow the instructions to verify your '
                  'email address.', 'info')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form)


@auth.route('/users/activate/<token>')
def activate(token):
    """Activate a user given a valid token."""
    try:
        user = db.session.query(User).filter_by(email_token=token).one()
        email = token_.confirm(token, current_app.config['SECRET_KEY'])
        if email != user.email:
            raise NoResultFound
    except NoResultFound:
        flash('Confirmation link is invalid or has expired.', 'danger')
    else:
        user = User.query.filter(User.email == email).one()
        if user.active:
            flash('Your account is already activated, please login.', 'info')
        else:
            user.active = True
            db.session.add(user)
            db.session.commit()
            flash('Your account has been activated. You can now login.',
                  'success')

    return redirect(url_for('auth.login'))
