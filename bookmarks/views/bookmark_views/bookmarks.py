"""Views for bookmark endpoints."""


from flask import abort, request, g
from flask_login import login_required
from flask_classy import FlaskView, route
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy.sql.expression import asc, desc
from werkzeug.exceptions import BadRequest

from main import db

from bookmarks.models import Bookmark, Category, Vote
from auth.models import User
from .utils import custom_render, serialize_models


class BookmarksView(FlaskView):
    """Gather all bookmark endpoints."""

    orders = {
        'new': desc(Bookmark.created_on), 'oldest': asc(Bookmark.created_on),
        'top': desc(Bookmark.rating), 'unpopular': asc(Bookmark.rating)}
    ordering_by = orders['new']

    def before_request(self, request_name, *args, **kwargs):
        """Order bookmarks if order_by was passed in request."""
        if 'order_by' in request.args:
            self.ordering_by = self.orders.get(request.args['order_by'])

    @route('/')
    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def get_bookmarks(self):
        """
        Return all bookmarks serialized with the category name.

        Join the users that submitted the bookmarks.
        If user is logged in, join possible votes he submitted.
        """
        if g.user.is_authenticated():
            query = db.session.query(Bookmark, User, Vote).join(
                User).outerjoin(Vote, Vote.bookmark_id == Bookmark._id)
        else:
            query = db.session.query(Bookmark, User).join(User)
        if self.ordering_by is not None:
            query = query.order_by(self.ordering_by)

        bookmarks = serialize_models(query)
        return (bookmarks, 'all')

    @route('/categories')
    @custom_render('bookmarks/list_categories.html', check_thumbnails=False)
    def get_categories(self):
        """Return paginator with all categories."""
        query = db.session.query(
            Category.name, func.count(Bookmark.category_id)).filter(
                Bookmark.category_id == Category._id).group_by(Category._id)
        return (query, 'all')

    @route('/categories/<name>')
    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def get_bookmarks_by_category(self, name):
        """
        Return paginator with bookmarks according to category name.

        Join the users that submitted the bookmarks.
        If user is logged in, join possible votes he submitted.
        """
        try:
            category = db.session.query(Category).filter_by(name=name).one()
        except NoResultFound:
            abort(404)
        if g.user.is_authenticated():
            query = db.session.query(Bookmark, User, Vote).filter(
                Bookmark.category_id == category._id).join(User).outerjoin(
                    Vote, Vote.bookmark_id == Bookmark._id)
        else:
            query = db.session.query(Bookmark, User).filter(
                Bookmark.category_id == category._id).join(User)
        if self.ordering_by is not None:
            query = query.order_by(self.ordering_by)
        bookmarks = serialize_models(query)
        return (bookmarks, name)

    @route('/<title>/vote', methods=['POST'])
    @login_required
    def vote_bookmark(self, title):
        """Vote up/down bookmark."""
        vote_direction = request.json.get('vote')
        if vote_direction not in range(-1, 2):
            raise BadRequest
        values = {-1: False, 0: None, 1: True}
        change = vote_direction
        try:
            bookmark = db.session.query(Bookmark).filter_by(title=title).one()
            vote = db.session.query(Vote).filter_by(
                user_id=g.user._id, bookmark_id=bookmark._id).one()
            if vote.direction is not None and vote_direction:
                vote.direction = values[vote_direction]
                change = 2 * vote_direction
            elif vote.direction is None and vote_direction:
                # From no rating, add the new one
                vote.direction = values[vote_direction]
                change = vote_direction
            else:
                # Revert back from -1 or +1 to 0
                if not vote.direction:
                    change = 1
                else:
                    change = -1
                vote.direction = values[vote_direction]

        except NoResultFound:
            # Theres no vote record for this bookmark so create one.
            vote = Vote(direction=values[vote_direction], user_id=g.user._id,
                        bookmark_id=bookmark._id)
        try:
            bookmark = db.session.query(Bookmark).filter(
                Bookmark._id == bookmark._id).one()
        except NoResultFound:
            abort(404)
        try:
            bookmark.rating += change
            db.session.add_all([vote, bookmark])
            db.session.commit()
        except Exception:
            db.session.rollback()
        return str(bookmark.rating)
