from flask import request, jsonify, url_for, g
from flask.views import MethodView

from bookmarks import csrf
from bookmarks.models import Bookmark, Favourite, FavouriteSchema
from bookmarks.logic import _save, _unsave

from .auth import token_auth


class FavouritesAPI(MethodView):

    decorators = [token_auth.login_required, csrf.exempt]

    def get(self, id):
        """Return all user's bookmark favourites."""
        if id is None:
            favourites = FavouriteSchema().dump(g.user.favourites.all(), many=True)
            return jsonify(favourites=favourites), 200

        favourite = Favourite.query.get(id)
        if favourite is None:
            return jsonify(message='favourite not found', status=404), 404
        if favourite.user_id != g.user.id:
            return jsonify(message='forbidden', status=403), 403

        return FavouriteSchema().jsonify(favourite), 200

    def post(self):
        """Add a bookmark to user's favourites."""
        payload = request.get_json() or {}
        if not payload:
            return jsonify(message='bad data', status=400), 400
        bookmark_id = payload.get('bookmark_id')
        bookmark = Bookmark.query.get(bookmark_id)
        if bookmark is None:
            return jsonify(message='bookmark not found', status=404), 404
        elif bookmark.user_id != g.user.id:
            return jsonify(message='forbidden', status=403), 403
        elif Favourite.query.filter_by(user_id=g.user.id,
                                       bookmark_id=bookmark_id).scalar() is not None:
            return jsonify(message='bookmark already saved', status=409), 409
        favourite_id = _save(bookmark_id)
        response = jsonify({})
        response.status_code = 201
        response.headers['Location'] = url_for(
            'favourites_api',
            id=favourite_id,
            _method='GET',
            _external=True
        )
        return response

    def delete(self, id):
        """Remove bookmark from user's favourites."""
        if Bookmark.query.get(id) is None:
            return jsonify(message='bookmark not found', status=404), 404
        favourite = Favourite.query.filter_by(user_id=g.user.id,
                                              bookmark_id=id).scalar()
        if favourite is None:
            return jsonify(message='save not found', status=404), 404
        _unsave(favourite)
        return jsonify({}), 204


favourites_api = FavouritesAPI.as_view('favourites_api')
