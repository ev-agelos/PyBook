"""Views for bookmark endpoints."""


from flask import abort, request, g, flash, redirect
from flask_login import login_required
from flask_classy import FlaskView, route
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy.sql.expression import asc, desc
from werkzeug.exceptions import BadRequest, Forbidden

from bookmarks import db

from ..models import Bookmark, Category, Vote, SaveBookmark
from .utils import custom_render


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
    def get(self):
        """Return all bookmarks with the category name."""
        query = db.session.query(Bookmark)
        if self.ordering_by is not None:
            query = query.order_by(self.ordering_by)

        return (query, 'all')

    @route('/categories/<name>')
    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def by_category(self, name):
        """Return paginator with bookmarks according to category name."""
        try:
            category = db.session.query(Category).filter_by(name=name).one()
        except NoResultFound:
            abort(404)
        query = db.session.query(Bookmark).filter(
            Bookmark.category_id == category.id)
        if self.ordering_by is not None:
            query = query.order_by(self.ordering_by)
        return (query, name)

    @route('/categories')
    @custom_render('bookmarks/list_categories.html', check_thumbnails=False)
    def get_categories(self):
        """Return paginator with all categories."""
        query = db.session.query(
            Category.name, func.count(Bookmark.category_id)).filter(
                Bookmark.category_id == Category.id).group_by(Category.id)
        return (query, 'all')

    @route('/search')
    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def search(self):
        """Search bookmarks."""
        flash('Sorry, search is not implemented yet :(', 'info')
        return ([], 'all')


    @route('/<title>/vote', methods=['POST'])
    @login_required
    def vote_bookmark(self, title):
        """Vote up/down bookmark."""
        vote_direction = request.json.get('vote')
        if vote_direction not in (-1, 1):
            raise BadRequest
        try:
            bookmark = db.session.query(Bookmark).filter_by(title=title).one()
        except NoResultFound:
            abort(404)
        else:
            if bookmark.vote is None:
                vote = Vote(user_id=g.user.id, bookmark_id=bookmark.id,
                            direction=False if vote_direction == -1  else True)
                db.session.add(vote)
                bookmark.rating += vote_direction
            else:
                if vote_direction == 1:  # Positive vote
                    if bookmark.vote.direction:
                        bookmark.vote.direction = None
                        bookmark.rating -= 1
                    else:
                        if bookmark.vote.direction is None:
                            bookmark.rating += 1
                        else:
                            bookmark.rating += 2
                        bookmark.vote.direction = True
                else:  # Negative vote
                    if bookmark.vote.direction == False:
                        bookmark.vote.direction = None
                        bookmark.rating += 1
                    else:
                        if bookmark.vote.direction is None:
                            bookmark.rating -= 1
                        else:
                            bookmark.rating -= 2
                        bookmark.vote.direction = False
        try:
            db.session.add(bookmark)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return str(bookmark.rating)

    @route('/<int:bookmark_id>/delete', methods=['DELETE', 'POST'])
    @login_required
    def delete(self, bookmark_id):
        """Endpoint to delete a bookmark."""
        bookmark = db.session.query(Bookmark).get(bookmark_id)
        if bookmark is None:
            abort(404)
        elif bookmark.user_id != g.user.id:
            raise Forbidden
        else:
            # Delete associated categories
            if db.session.query(Bookmark).filter_by(
                    category_id=bookmark.category_id).count() == 1:
                category = db.session.query(Category).get(bookmark.category_id)
                db.session.delete(category)
            # Delete associated votes
            db.session.query(Vote).filter_by(bookmark_id=bookmark_id).delete()
            # Delete associated saves
            db.session.query(SaveBookmark).filter_by(
                bookmark_id=bookmark_id).delete()
            db.session.delete(bookmark)
            db.session.commit()
        return redirect(request.referrer)
