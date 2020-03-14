"""API endpoints for bookmarks."""

from flask import jsonify, url_for, g
from flask.views import MethodView

from bookmarks import csrf
from bookmarks.models import Bookmark, BookmarkSchema
from bookmarks.forms import AddBookmarkForm, UpdateBookmarkForm
from bookmarks.logic import _get, _post, _put, _delete

from .auth import token_auth


class BookmarksAPI(MethodView):

    decorators = [token_auth.login_required, csrf.exempt]

    def get(self, id=None):
        """Return bookmark if id was given otherwise return all bookmarks."""
        if id is None:
            query = _get()
            bookmarks = BookmarkSchema().dump(query.all(), many=True)
            return jsonify(bookmarks=bookmarks), 200
        else:
            bookmark = Bookmark.query.get(id)
            if bookmark is None:
                return jsonify(message='Bookmark not found', status=404), 404
            return BookmarkSchema().jsonify(bookmark), 200

    def post(self):
        """Add new bookmark and add it's tags if don't exist."""
        form = AddBookmarkForm(meta={'csrf':False})
        if not form.validate():
            return jsonify(message='invalid data', status=400), 400
        bookmark = Bookmark.query.filter_by(url=form.url.data).scalar()
        if bookmark is not None:
            return jsonify(message='bookmark already exists', status=409), 409
        bookmark_id = _post(form)

        response = jsonify({})
        response.status_code = 201
        response.headers['Location'] = url_for(
            'bookmarks_api', id=bookmark_id, _method='GET', _external=True)
        return response

    def put(self, id):
        """
        Update a bookmark entry.

        In case tag(s) changes check if no other bookmark is related with
        that tag(s) and if not, delete it.
        """
        form = UpdateBookmarkForm(meta={'csrf':False})
        if not form.validate():
            return jsonify(message='invalid data', status=400), 400
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            return jsonify(message='Bookmark does not exist', status=404), 404
        if form.url.data and form.url.data != bookmark.url:
            existing_url = Bookmark.query.filter_by(url=form.url.data).scalar()
            if existing_url is not None:
                return jsonify(message='url already exists', status=409), 409
        _put(id, form)
        return jsonify(message='Bookmark updated', status=200), 200

    def delete(self, id):
        """Delete a bookmark."""
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            return jsonify(message='not found', status=404), 404
        if bookmark.user_id != g.user.id:
            return jsonify(message='forbidden', status=403), 403
        _delete(id)
        return jsonify({}), 204


bookmarks_api = BookmarksAPI.as_view('bookmarks_api')
