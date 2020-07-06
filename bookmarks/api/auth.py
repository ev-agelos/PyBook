"""Auth API endpoints."""


from flask import g
from flask_smorest import abort, Blueprint
from flask_login import login_required, logout_user

from bookmarks import csrf, db
from bookmarks.users.models import User


auth_api = Blueprint('auth_api', 'Auth', url_prefix='/api/v1/auth/',
                     description='Endpoints for logging in/out etc')


@auth_api.route('/request-token', methods=['POST'])
@csrf.exempt
@login_required
def request_token():
    """Return new token for the user."""
    if not g.user.active:
        abort(403, message='Email address is not verified yet.')
    # TODO check if need to call login_user, also research what authenticated = True does (cause it is not called)
    return {'token': g.user.generate_auth_token()}


@auth_api.route('/logout')
@csrf.exempt
@login_required
def logout():
    """Logout a user."""
    g.user.auth_token = ''
    g.user.authenticated = False
    logout_user()
    db.session.commit()
    return {}, 204
