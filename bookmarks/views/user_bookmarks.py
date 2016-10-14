"""User-bookmarks endpoints."""

from flask import g, request
from flask_login import login_required
from flask_classy import FlaskView, route

from bookmarks import db

from ..models import Category, Bookmark, SaveBookmark
from .utils import custom_render


class UsersView(FlaskView):
    """Endpoints for users resource."""

    @route('/<username>/bookmarks')
    @custom_render('bookmarks/user_links.html')
    @login_required
    def get_bookmarks(self, username):
        """
        Return user's bookmarks.
        
        They can be filtered by given request argument <category>.
        """
        name = request.args.get('category')
        if name:
            category = Category.query.filter_by(name=name).first_or_404()
            bookmarks = db.session.query(Bookmark).filter_by(
                user_id=g.user.id, category_id=category.id)
        else:
            bookmarks = db.session.query(Bookmark).filter_by(user_id=g.user.id)
        return (bookmarks, name)

    @route('/<username>/bookmarks/saved')
    @custom_render('bookmarks/saved_links.html')
    @login_required
    def get_saved(self, username):
        """Return user's saved bookmarks."""
        saves = db.session.query(SaveBookmark).filter_by(
            user_id=g.user.id).filter_by(is_saved=True).all()
        return ([saved.bookmark for saved in saves], 'saved')
