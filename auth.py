"""Module to handle login/logout/register functions."""

from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from app import db
from models import User
from forms import LoginForm


login_page = Blueprint('login_page', __name__, template_folder='templates')
logout_page = Blueprint('logout_page', __name__, template_folder='templates')


@login_page.route('/login', methods=['GET', 'POST'])
def login():
    """Login to application."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(**form.data).first()
        if user:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Login was successful!')
            return redirect(url_for('index'))
        else:
            flash('Wrong credentials!')
    return render_template('login.html', form=form)


@logout_page.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.commit()
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
