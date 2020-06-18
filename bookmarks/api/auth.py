"""Auth API endpoints."""


from flask import Blueprint, g, jsonify
from flask_login import login_required

from bookmarks import csrf
from bookmarks.users.models import User


auth_api = Blueprint('api', __name__)


@auth_api.route('/api/v1/auth/request-token', methods=['POST'])
@csrf.exempt
@login_required
def request_token():
    """Return new token for the user."""
    return jsonify({'token': g.user.generate_auth_token()}), 200
