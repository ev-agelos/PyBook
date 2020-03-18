"""API endpoints for bookmarks."""

from flask import url_for, g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from bookmarks import csrf
from bookmarks.models import Bookmark
from bookmarks.logic import _get, _post, _put, _delete

from .auth import token_auth
from .schemas import (
    BookmarkSchema,
    BookmarkPOSTSchema,
    BookmarkPUTSchema,
    BookmarksQueryArgsSchema
)


bookmarks_api = Blueprint('bookmarks_api', 'Bookmarks', url_prefix='/api/v1/bookmarks/',
                          description='Operations on Bookmarks')


@bookmarks_api.route('/')
class BookmarksAPI(MethodView):

    decorators = [csrf.exempt, token_auth.login_required]

    @bookmarks_api.arguments(BookmarksQueryArgsSchema, location='query')
    @bookmarks_api.response(BookmarkSchema(many=True))
    def get(self, args):
        """Return all bookmarks of the authenticated user."""
        query = _get(args)
        return query.all()

    @bookmarks_api.arguments(BookmarkPOSTSchema)
    def post(self, data):
        """Add new bookmark and add its tags if don't exist."""
        bookmark = Bookmark.query.filter_by(url=data['url']).scalar()
        if bookmark is not None:
            abort(409, message='Url already exists')
        bookmark_id = _post(data)
        bookmark_url = url_for(
            'bookmarks_api.BookmarkAPI',
            id=bookmark_id,
            _method='GET',
            _external=True
        )
        return {}, 201, {'Location': bookmark_url}


@bookmarks_api.route('/<int:id>')
class BookmarkAPI(MethodView):

    decorators = [csrf.exempt, token_auth.login_required]

    @bookmarks_api.response(BookmarkSchema())
    def get(self, id):
        """Return bookmark."""
        return Bookmark.query.get(id) or abort(404)

    @bookmarks_api.arguments(BookmarkPUTSchema)
    @bookmarks_api.response(BookmarkSchema())
    def put(self, data, id):
        """
        Update an existing bookmark.

        In case tag(s) changes check if no other bookmark is related with
        that tag(s) and if not, delete it.
        """
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            abort(404, message='Bookmark not found')
        if 'url' in data and data['url'] != bookmark.url:
            existing_url = Bookmark.query.filter_by(url=data['url']).scalar()
            if existing_url is not None:
                abort(409, message='New url already exists')
        _put(id, data)
        return Bookmark.query.get(id)

    @bookmarks_api.response(code=204)
    def delete(self, id):
        """Delete a bookmark."""
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            abort(404, message='Bookmark not found')
        if bookmark.user_id != g.user.id:
            abort(403, message='Forbidden')
        _delete(id)
