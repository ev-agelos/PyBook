"""Module to handle login/logout/register functions."""

from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from flask import session

from bookmarks import db
from bookmarks.models import User
from bookmarks.forms import LoginForm, RegistrationForm


login_Bp = Blueprint('login_page', __name__, template_folder='templates')
logout_Bp = Blueprint('logout_page', __name__, template_folder='templates')
register_Bp = Blueprint('register_page', __name__, template_folder='templates')


@login_Bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login to application."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_password_correct(form.password.data):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=form.remember_me.data)
            print(session.items())
            flash('Login was successful!')
            return redirect(url_for('home'))
        else:
            flash('Wrong credentials!')
    return render_template('login.html', form=form)


@logout_Bp.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    current_user.authenticated = False
    db.session.commit()
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@register_Bp.route('/register', methods=['GET', 'POST'])
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
            flash('Username is already taken!')
        elif email_exists:
            flash('Email is already taken!')
        else:
            user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
    return render_template('register.html', form=form)