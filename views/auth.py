"""Module to handle login/logout/register functions."""

from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from flask import session

from app import db, bcrypt
from models import User
from forms import LoginForm, RegistrationForm


login_Bp = Blueprint('login_page', __name__, template_folder='templates')
logout_Bp = Blueprint('logout_page', __name__, template_folder='templates')
register_Bp = Blueprint('register_page', __name__, template_folder='templates')


@login_Bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login to application."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
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
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)
