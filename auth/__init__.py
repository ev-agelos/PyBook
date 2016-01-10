"""Module to handle login/logout/register functions."""


from flask import (request, url_for, redirect, render_template, flash, g,
                   Blueprint)
from flask_login import login_user, logout_user, login_required

from bookmarks_app import db
from bookmarks_app.models import User
from bookmarks_app.forms import LoginForm, RegistrationForm


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login to application."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and user.is_password_correct(form.password.data):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            flash('Login was successful.', 'success')
            return redirect(url_for('index.home'))
        else:
            flash('Wrong credentials!', 'danger')
    return render_template('login.html', form=form)


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
            user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index.home'))
    return render_template('register.html', form=form)