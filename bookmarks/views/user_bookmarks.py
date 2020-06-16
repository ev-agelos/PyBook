"""User-bookmarks endpoints."""

from flask import g, request, render_template, Blueprint
from werkzeug.exceptions import Forbidden
from flask_login import login_required
from ..models import Tag, Bookmark, tags_bookmarks
from ..forms import AddBookmarkForm


bookmarks_per_user = Blueprint('bookmarks_per_user', __name__)


@bookmarks_per_user.route('/users/<username>/bookmarks/saved')
@login_required
def get_saved(username):
    """Return user's saved bookmarks."""
    fav_ids = [fav.bookmark_id for fav in g.user.favourites]
    bookmarks = Bookmark.query.filter(Bookmark.id.in_(fav_ids))
    pag = bookmarks.paginate(page=request.args.get('page', 1), per_page=5)
    return render_template('bookmarks/favourites.html', paginator=pag)


@bookmarks_per_user.route('/users/<username>/bookmarks/subscriptions')
@login_required
def get_subscriptions(username):
    """Return user's subscribed bookmarks."""
    if username != g.user.username:
        raise Forbidden
    subscribed_ids = [user.id for user in g.user.subscribed.all()]
    bookmarks = Bookmark.query.filter(Bookmark.user_id.in_(subscribed_ids))
    pag = bookmarks.paginate(page=request.args.get('page', 1, int), per_page=5)
    return render_template('bookmarks/list_bookmarks.html', paginator=pag,
                           form=AddBookmarkForm())
