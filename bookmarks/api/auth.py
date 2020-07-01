"""Auth API endpoints."""


from flask import Blueprint, g, jsonify
from flask_login import login_required, logout_user

from bookmarks import csrf, db
from bookmarks.users.models import User


auth_api = Blueprint('api', __name__)


@auth_api.route('/api/v1/auth/request-token', methods=['POST'])
@csrf.exempt
@login_required
def request_token():
    """Return new token for the user."""
    return jsonify({'token': g.user.generate_auth_token()}), 200


@auth_api.route('/api/v1/auth/logout')
@csrf.exempt
@login_required
def logout():
    """Logout a user."""
    g.user.auth_token = ''
    g.user.authenticated = False
    logout_user()
    db.session.commit()
    return {}, 204
