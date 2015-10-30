"""User endpoint views."""

from flask import render_template, abort, g
from flask_classy import FlaskView, route
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from bookmarks_app import db
from bookmarks_app.models import User, Category, Bookmark, Vote
from .utils import paginate


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
    def get_categories_by_user(self, username):
        """Return paginator with all user's categories."""
        try:
            user = db.query(User).filter_by(username=username).one()
        except NoResultFound:
            abort(404)
        categories = db.query(
            Category.name, func.count(Bookmark.category_id)).filter(
                Bookmark.category_id == Category._id,
                Bookmark.user_id == user._id).group_by(Category._id)
        return render_template('list_categories.html',
                               categories=paginate(categories))

    @route('/<username>/categories/<name>')
    def get_user_bookmarks_by_category(self, username, name):
        """Return user's bookmarks according to category <name>."""
        try:
            user = db.query(User).filter_by(username=username).one()
            category = db.query(Category).filter_by(name=name).one()
        except NoResultFound:
            abort(404)
        if g.user.is_authenticated():
            bookmarks = db.query(Bookmark, User, Vote).filter(
                Bookmark.user_id == user._id).filter_by(
                    category_id=category._id).join(User).outerjoin(
                        Vote, Vote.bookmark_id == Bookmark._id)
        else:
            bookmarks = db.query(Bookmark, User).filter(
                Bookmark.user_id == user._id).filter_by(
                    category_id=category._id).join(User)

        return render_template('list_bookmarks.html',
                               bookmarks=paginate(bookmarks),
                               category_name=name)

    @route('/<username>/bookmarks/<title>')
    def get_user_bookmark_by_title(self, username, title):
        """Return user's bookmark according to title passed."""
        try:
            user = db.query(User).filter_by(username=username).one()
        except NoResultFound:
            abort(404)
        bookmark_user = db.query(Bookmark, User).filter(
            Bookmark.user_id == user._id).filter(Bookmark.title == title).join(
                User).paginate(page=1, per_page=1)
        category_name = ''
        if bookmark_user.showing:
            category_name = db.query(Category).get(
                bookmark_user.items[0][0].category_id).name
        return render_template('list_bookmarks.html',
                               category_name=category_name,
                               bookmarks=bookmark_user)

    @route('/<username>/bookmarks/')
    def get_all_user_bookmarks(self, username):
        """Return all user's bookmarks."""
        try:
            user = db.query(User).filter_by(username=username).one()
        except NoResultFound:
            abort(404)
        if g.user.is_authenticated():
            bookmarks = db.query(Bookmark, User, Vote).join(User).filter(
                Bookmark.user_id == user._id).outerjoin(
                    Vote, Vote.bookmark_id == Bookmark._id)
        else:
            bookmarks = db.query(Bookmark, User).join(User).filter(
                Bookmark.user_id == user._id)
        return render_template('list_bookmarks.html', category_name='all',
                               bookmarks=paginate(bookmarks))
