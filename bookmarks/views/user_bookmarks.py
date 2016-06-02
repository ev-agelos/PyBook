"""User-bookmarks endpoints."""

from flask import abort, g, request
from flask_login import login_required
from flask_classy import FlaskView, route
from sqlalchemy import func, desc, asc
from sqlalchemy.orm.exc import NoResultFound

from main import db

from auth.models import User

from ..models import Category, Bookmark, SaveBookmark
from .utils import custom_render



class UsersView(FlaskView):
    """Bookmarks specific to user."""

    orders = {
        'new': desc(Bookmark.created_on), 'oldest': asc(Bookmark.created_on),
        'top': desc(Bookmark.rating), 'unpopular': asc(Bookmark.rating)}
    ordering_by = orders['new']

    @route('/<username>/categories')
    @custom_render('bookmarks/list_categories.html')
    def get_user_categories(self, username):
        """Return paginator with all user's categories."""
        if g.user.is_authenticated and username == g.user.username:
            user = g.user
        else:
            try:
                user = db.session.query(User).filter_by(
                    username=username).one()
            except NoResultFound:
                abort(404)
        categories = db.session.query(
            Category.name, func.count(Bookmark.category_id)).filter(
                Bookmark.category_id == Category._id,
                Bookmark.user_id == user._id).group_by(Category._id)
        return (categories, 'all')

    @route('/<username>/categories/<name>')
    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def get_user_bookmarks_by_category(self, username, name):
        """Return user's bookmarks according to category <name>."""
        try:
            if g.user.is_authenticated and username == g.user.username:
                user = g.user
            else:
                user = db.session.query(User).filter_by(
                    username=username).one()

            if name != 'all':
                category = db.session.query(Category).filter_by(
                    name=name).one()
        except NoResultFound:
            abort(404)

        bookmarks = db.session.query(Bookmark).filter(
            Bookmark.user_id == user._id)
        if name != 'all':
            bookmarks = bookmarks.filter(Bookmark.category_id == category._id)
        return (bookmarks, name)

    @route('/<username>/bookmarks')
    @route('/<username>/bookmarks/<title>')
    @custom_render('bookmarks/list_bookmarks.html')
    def get_user_bookmark_by_title(self, username, title=None):
        """Return user's bookmark according to title passed."""
        if g.user.is_authenticated and username == g.user.username:
            user = g.user
        else:
            try:
                user = db.session.query(User).filter_by(
                    username=username).one()
            except NoResultFound:
                abort(404)
        if title is not None:
            try:
                bookmarks = [db.session.query(Bookmark).filter(
                    Bookmark.user_id == user._id).filter(
                        Bookmark.title == title).one()]
            except NoResultFound:
                abort(404)
            category_name = db.session.query(Category).get(
                bookmarks[0].category_id).name
        else:
            category_name = 'all'
            bookmarks = db.session.query(Bookmark).filter(
                Bookmark.user_id == user._id)
        return (bookmarks, category_name)

    @route('/<username>/saved')
    @login_required
    @custom_render('bookmarks/list_bookmarks.html')
    def get_user_saved_bookmarks(self, username):
        """Return user's saved bookmarks."""
        ordering_by = self.orders.get(request.args.get('order_by'),
                                      self.orders['new'])
        saves = db.session.query(SaveBookmark).filter_by(
            user_id=g.user._id).filter_by(is_saved=True)
        bookmarks = [result.bookmark for result in saves]
        return (bookmarks, 'saved')
