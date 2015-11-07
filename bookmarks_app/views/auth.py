"""Module to handle login/logout/register functions."""

from flask import request, url_for, redirect, render_template, flash, g
from flask_login import login_user, logout_user, login_required

from bookmarks_app import db, app
from bookmarks_app.models import User
from bookmarks_app.forms import LoginForm, RegistrationForm


@app.route('/login', methods=['GET', 'POST'])
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
            flash('success', 'Login was successful.')
            return redirect(url_for('home'))
        else:
            flash('danger', 'Wrong credentials!')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    g.user.authenticated = False
    db.session.commit()
    logout_user()
    flash('info', 'You have been logged out.')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    form = RegistrationForm()
    if form.validate_on_submit():
        username_exists = db.session.query(User).filter_by(
            username=form.username.data).first()
        email_exists = db.session.query(User).filter_by(
            email=form.email.data).first()
        if username_exists and email_exists:
            flash('warning', 'Username and email are already taken!')
        elif username_exists:
            flash('warning', 'Username is already taken!')
        elif email_exists:
            flash('warning', 'Email is already taken!')
        else:
            user = User(username=form.username.data, email=form.email.data,
                        password=form.password.data)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
    return render_template('register.html', form=form)
