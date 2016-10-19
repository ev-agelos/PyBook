"""User-bookmarks endpoints."""

from flask import g, request
from flask_login import login_required
from flask_classy import FlaskView, route

from ..models import Category, Bookmark
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
            bookmarks = g.user.bookmarks.filter_by(category_id=category.id)
        else:
            bookmarks = g.user.bookmarks
        return (bookmarks, name)

    @route('/<username>/bookmarks/saved')
    @custom_render('bookmarks/favourites.html')
    @login_required
    def get_saved(self, username):
        """Return user's saved bookmarks."""
        fav_ids = [fav.bookmark_id for fav in g.user.favourites]
        favourites = g.user.bookmarks.filter(Bookmark.id.in_(fav_ids))
        return (favourites, 'saved')
