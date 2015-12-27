"""User endpoint views."""

from flask import render_template, abort, g
from flask_classy import FlaskView, route
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from bookmarks_app import db
from bookmarks_app.models import User, Category, Bookmark, Vote
from .utils import paginate, custom_render, serialize_models


class UsersView(FlaskView):
    """Bookmarks specific to user."""

    @route('/')
    def get_users(self):
        """Return all users."""
        users = db.session.query(User).all()
        return render_template('list_users.html', users=users)

    @route('/<username>')
    def get_user(self, username=''):
        """Return all users."""
        if username:
            try:
                user = db.session.query(User).filter_by(
                    username=username).one()
            except NoResultFound:
                abort(404)
            return render_template('profile.html', user=user)
        else:
            abort(404)

    @route('/<username>/categories')
    @custom_render('list_categories.html')
    def get_user_categories(self, username):
        """Return paginator with all user's categories."""
        try:
            user = db.query(User).filter_by(username=username).one()
        except NoResultFound:
            abort(404)
        categories = db.query(
            Category.name, func.count(Bookmark.category_id)).filter(
                Bookmark.category_id == Category._id,
                Bookmark.user_id == user._id).group_by(Category._id)
        categories = serialize_models(categories)
        return (categories, 'all')

    @route('/<username>/categories/<name>')
    @custom_render('list_bookmarks.html', check_thumbnails=True)
    def get_user_bookmarks_by_category(self, username, name):
        """Return user's bookmarks according to category <name>."""
        user = None
        if g.user.is_authenticated() and username == g.user.username:
            user = g.user
        try:
            if user is None:
                user = db.query(User).filter_by(username=username).one()
            if name != 'all':
                category = db.query(Category).filter_by(name=name).one()
        except NoResultFound:
            abort(404)

        if name == 'all':
            bookmarks = db.query(Bookmark, User, Vote).filter(
                Bookmark.user_id == user._id).join(User).outerjoin(
                    Vote, Vote.bookmark_id == Bookmark._id)
        else:
            bookmarks = db.query(Bookmark, User, Vote).filter(
                Bookmark.user_id == user._id).filter_by(
                    category_id=category._id).join(User).outerjoin(
                        Vote, Vote.bookmark_id == Bookmark._id)
        bookmarks = serialize_models(bookmarks)
        return (bookmarks, name)

    @route('/<username>/bookmarks/<title>')
    @custom_render('list_bookmarks.html')
    def get_user_bookmark_by_title(self, username, title):
        """Return user's bookmark according to title passed."""
        try:
            user = db.query(User).filter_by(username=username).one()
            bookmark_user = db.query(Bookmark, User).filter(
                Bookmark.user_id == user._id).filter(
                    Bookmark.title == title).join(User).one()
        except NoResultFound:
            abort(404)
        category_name = db.query(Category).get(
            bookmark_user[0].category_id).name
        bookmark_user = serialize_models(bookmark_user)
        return (bookmark_user, category_name)
