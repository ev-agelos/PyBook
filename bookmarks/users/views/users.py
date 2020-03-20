"""User endpoints."""

from flask import (render_template, g, Blueprint, abort, jsonify, redirect,
                   url_for, flash, current_app)
from flask_login import login_required
from werkzeug.exceptions import BadRequest, Forbidden

from bookmarks import db, utils

from ..models import User
from ..forms import ProfileForm, ChangePasswordForm

users = Blueprint('users', __name__)


@users.route('/users/')
@users.route('/users/<int:id>')
def get_users(id=None):
    """Return all users or the user with the given <id>."""
    if id is None:
        users = db.session.query(User).all()
        return render_template('auth/list_users.html', users=users)

    if g.user.is_authenticated and id == g.user.id:
        user = g.user
        form = ProfileForm(obj=g.user)
    else:
        user = User.query.get(id)
        if user is None:
            abort(404)
        form = ProfileForm(formdata=None)
    password_form = ChangePasswordForm()
    return render_template('auth/profile.html', user=user, profile_form=form,
                           password_form=password_form)


@users.route('/users/<int:id>/subscribe', methods=['POST'])
@login_required
def subscribe(id):
    """Subscribe to a user."""
    if id == g.user.id:
        raise BadRequest
    user = User.query.get(id)
    if user is None:
        abort(404)
    subscription = g.user.subscribe(user)
    if subscription is None:
        raise BadRequest
    db.session.add(subscription)
    db.session.commit()
    response = jsonify({})
    response.status_code = 201
    return response


@users.route('/users/<int:id>/unsubscribe', methods=['DELETE'])
@login_required
def unsubscribe(id):
    """Unsubscribe from a user."""
    if id == g.user.id:
        raise BadRequest
    user = User.query.get(id)
    if user is None:
        abort(404)
    subscription = g.user.unsubscribe(user)
    if subscription is None:
        raise BadRequest
    db.session.add(subscription)
    db.session.commit()
    return jsonify({}), 204


@users.route('/users/<int:id>/update-password', methods=['POST'])
@login_required
def update_password(id):
    """Update user's password."""
    if id != g.user.id:
        raise Forbidden
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not g.user.is_password_correct(form.password.data):
            flash('Current password is not valid.', 'danger')
        else:
            g.user.password = form.new_password.data
            db.session.add(g.user)
            db.session.commit()
            flash('Password updated successfully.', 'success')
            text = (
                'The password for your PyBook account on <a href="{}">{}</a> '
                'has successfully\nbeen changed.\n\nIf you did not initiate '
                'this change, please contact the administrator immediately.'
            ).format(request.host_url, request.host_url)
            utils.send_email('Password changed', g.user.email, text)
            return redirect(url_for('auth.logout'))

    profile_form = ProfileForm(formdata=None, obj=g.user)
    return render_template('auth/profile.html', user=g.user,
                           password_form=form, profile_form=profile_form)


@users.route('/users/<int:id>/update-profile', methods=['POST'])
@login_required
def update_profile(id):
    """Update user's profile settings."""
    if id != g.user.id:
        raise Forbidden
    form = ProfileForm()
    password_form = ChangePasswordForm(formdata=None)
    if not form.validate_on_submit():
        return redirect(url_for('users.get_users', username=g.user.username))
    if form.username.data != g.user.username:
        user = User.query.filter_by(username=form.username.data).scalar()
        if user is not None:
            flash('Username has already been taken.', 'danger')
            return render_template('auth/profile.html', user=g.user,
                                   password_form=password_form,
                                   profile_form=form)
        g.user.username = form.username.data
        flash('Profile updated successfully.', 'success')

    if form.email.data != g.user.email:
        user = User.query.filter_by(email=form.email.data).scalar()
        if user is not None:
            flash('Email address already exists.', 'danger')
            return redirect(url_for('users.get_users',
                                    username=g.user.username))
        g.user.auth_token = g.user.generate_auth_token(email=form.email.data)
        activation_link = url_for('auth.confirm', token=g.user.auth_token,
                                  _external=True)
        text = ('Click the link to confim your email address:\n' +
                str(activation_link))
        sent = utils.send_email('Email change confirmation - PyBook',
                                form.email.data, text)
        if sent:
            flash('A verification email has been sent to <{}>'
                  .format(form.email.data), 'info')

    db.session.add(g.user)
    db.session.commit()
    return redirect(url_for('users.get_users', id=g.user.id))
