from flask import request, jsonify, url_for, g
from flask.views import MethodView
from flask_login import login_required
from flask_smorest import Blueprint, abort

from bookmarks import csrf
from bookmarks.models import Bookmark, Favourite
from bookmarks.logic import _save, _unsave

from .schemas import FavouriteSchema, FavouritePOSTSchema


favourites_api = Blueprint('favourites_api', 'Favourites', url_prefix='/api/v1/favourites/',
                           description='Operations on Favourites')


@favourites_api.route('/')
class FavouritesAPI(MethodView):

    decorators = [login_required, csrf.exempt]

    @favourites_api.response(FavouriteSchema(many=True))
    def get(self):
        """Return all user's bookmark favourites."""
        return g.user.favourites.all()

    @favourites_api.arguments(FavouritePOSTSchema)
    def post(self, args):
        """Add a bookmark to user's favourites."""
        bookmark = Bookmark.query.get(args['bookmark_id'])
        if bookmark is None:
            abort(404, message='bookmark not found')
        elif bookmark.user_id == g.user.id:
            abort(403, message='forbidden')
        elif Favourite.query.filter_by(user_id=g.user.id,
                                       bookmark_id=bookmark.id).scalar() is not None:
            abort(409, message='bookmark already saved')

        _save(bookmark.id)
        return {}, 201


@favourites_api.route('/<int:id>')
class FavouriteAPI(MethodView):

    decorators = [csrf.exempt, login_required]

    @favourites_api.response(code=204)
    def delete(self, id):
        """Remove bookmark from user's favourites."""
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            abort(404, message='Bookmark not found')
        favourite = Favourite.query.filter_by(user_id=g.user.id,
                                              bookmark_id=id).scalar()
        if favourite is None:
            abort(404, message='Favourite not found')
        _unsave(favourite)
