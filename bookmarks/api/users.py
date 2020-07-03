"""API endpoints for users."""


from flask import g, url_for, request
from flask.views import MethodView
from flask_login import login_required
from flask_smorest import abort, Blueprint

from bookmarks import db, csrf
from bookmarks import utils
from bookmarks.users.models import User
from .schemas import UserPUTSchema, UserSchema


users_api = Blueprint('users_api', 'Users', url_prefix='/api/v1/users/',
                      description='Operations on Users')


@users_api.route('/me')
@users_api.response(UserSchema())
@csrf.exempt
@login_required
def me():
    return g.user


@users_api.route('/')
class UsersAPI(MethodView):

    decorators = [csrf.exempt]

    @users_api.response(UserSchema(many=True, exclude=("email", )))
    def get(self):
        """Return all users."""
        return User.query.all()


@users_api.route('/<int:id>')
class UserAPI(MethodView):

    decorators = [csrf.exempt, login_required]

    @users_api.response(UserSchema(exclude=("email", )))
    def get(self, id):
        """Return user with given id."""
        return (
            id == g.user.id and g.user
            or User.query.get(id)
            or abort(404, message='User not found')
        )

    @users_api.arguments(UserPUTSchema)
    @users_api.response(code=204)
    def put(self, data, id):
        """Update an existing user."""
        id != g.user.id and abort(403)

        if data.get('username') and data['username'] != g.user.username:
            if User.query.filter_by(username=data['username']).scalar():
                abort(409, message='Username already taken')
            g.user.username = data['username']
        if data.get('email') and data['email'] != g.user.email:
            if User.query.filter_by(email=data['email']).scalar():
                abort(409, message='Email already taken')
            # XXX it should revoke current API connection
            g.user.auth_token = g.user.generate_auth_token(email=data['email'])
            activation_link = url_for('auth.confirm', token=g.user.auth_token,
                                      _external=True)
            text = f'Click the link to confim your email address:\n{activation_link}'
            sent = utils.send_email('Email change confirmation - PyBook',
                                    data['email'], text)
            # if sent:
            #     message = f'A verification email has been sent to <{email}>'
        if any(key in data for key in ('currentPassword', 'newPassword', 'confirmPassword')):
            if data['newPassword'] == '':
                abort(409, message="New password must not be empty")
            if data['newPassword'] != data['confirmPassword']:
                abort(409, message='Passwords differ')
            if not g.user.is_password_correct(data['currentPassword']):
                abort(409, message='Current password is wrong')
            g.user.auth_token = ''
            g.user.password = data['newPassword']
            text = (
                'The password for your PyBook account on <a href="{}">{}</a> '
                'has successfully\nbeen changed.\n\nIf you did not initiate '
                'this change, please contact the administrator immediately.'
            ).format(request.host_url, request.host_url)
            utils.send_email('Password changed', g.user.email, text)

        db.session.add(g.user)
        db.session.commit()
