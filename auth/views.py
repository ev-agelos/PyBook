"""Module to handle login/logout/register functions."""


from flask import (request, url_for, redirect, render_template, flash, g,
                   Blueprint)
from flask_login import login_user, logout_user, login_required
from flask_mail import Message

from main import db, mail

from .forms import LoginForm, RegistrationForm
from .models import User
from .token import generate_user_token, confirm_token


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
                return redirect(url_for('index.home'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    g.user.authenticated = False
    db.session.commit()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    form = RegistrationForm()
    if form.validate_on_submit():
        username_exists = db.session.query(User).filter_by(
            username=form.username.data).first()
        email_exists = db.session.query(User).filter_by(
            email=form.email.data).first()
        if username_exists and email_exists:
            flash('Username and email are already taken!')
        elif username_exists:
            flash('Username is already taken!', 'warning')
        elif email_exists:
            flash('Email is already taken!', 'warning')
        else:
            token = generate_user_token(form.email.data)
            user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            activation_link = url_for('auth.activate', token=token,
                                      _external=True)
            msg = Message(
                subject='Account confirmation - Python Bookmarks',
                body='Welcome {},\n\nactivate your account by clicking this '
                     'link: {}'.format(user.username, activation_link),
                recipients=[user.email])
            mail.send(msg)
            flash('A verification email has been sent to the registered email '
                  'address. Please follow the instructions to verify your '
                  'email address.', 'info')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form)


@auth.route('/users/activate/<token>')
def activate(token):
    """Activate a user given a valid token."""
    email = confirm_token(token)
    if email:
        user = User.query.filter(User.email==email).one()
        if user.active:
            flash('Your account is already activated, please login.', 'info')
        else:
            user.active = True
            db.session.add(user)
            db.session.commit()
            flash('Your account has been activated. You can now login.',
                  'success')
    else:
        flash('Confirmation link is invalid or has expired.', 'danger')

    return redirect(url_for('auth.login'))
