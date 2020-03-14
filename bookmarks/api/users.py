"""API endpoints for users."""


from flask import g, jsonify
from flask.views import MethodView

from bookmarks import db, csrf
from bookmarks.users.models import User, UserSchema

from .auth import token_auth


class UsersAPI(MethodView):

    decorators = [csrf.exempt, token_auth.login_required]

    def get(self, id=None):
        """Get a user given an id or get all users."""
        if id is None:
            users = UserSchema().dump(User.query.all(), many=True)
            return jsonify(users=users), 200

        if id == g.user.id:
            return UserSchema().jsonify(g.user), 200

        user = User.query.get(id)
        if user is None:
            return jsonify(message='User not found', status=404), 404
        return UserSchema().jsonify(user), 200

    def put(self, id):
        """Update an existing user."""
        pass

    def delete(self, id):
        """Delete an existing user and his favourites."""
        if id != g.user.id:
            return jsonify(message='forbidden', status=403), 403
        db.session.delete(g.user)
        db.session.commit()
        return jsonify({}), 204


users_api = UsersAPI.as_view('users_api')
