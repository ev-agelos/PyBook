"""User-bookmarks endpoints."""

from flask import g, request, render_template, Blueprint
from flask_login import login_required
from ..models import Category, Bookmark


bookmarks_per_user = Blueprint('bookmarks_per_user', __name__)


@bookmarks_per_user.route('/users/<username>/bookmarks')
@login_required
def get_bookmarks(username):
    """
    Return user's bookmarks.

    They can be filtered by given request argument <category>.
    """
    name = request.args.get('category')
    if name:
        category = Category.query.filter_by(name=name).first_or_404()
        bookmarks = Bookmark.query.filter_by(user_id=g.user.id,
                                             category_id=category.id)
    else:
        bookmarks = Bookmark.query.filter_by(user_id=g.user.id)
    pag = bookmarks.paginate(page=request.args.get('page', 1), per_page=5)
    return render_template('bookmarks/user_links.html', paginator=pag,
                           category=name)


@bookmarks_per_user.route('/users/<username>/bookmarks/saved')
@login_required
def get_saved(username):
    """Return user's saved bookmarks."""
    fav_ids = [fav.id for fav in g.user.favourites]
    bookmarks = Bookmark.query.filter(Bookmark.id.in_(fav_ids))
    pag = bookmarks.paginate(page=request.args.get('page', 1), per_page=5)
    return render_template('bookmarks/favourites.html', paginator=pag,
                           category='saved')
