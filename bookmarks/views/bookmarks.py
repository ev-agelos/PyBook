"""Views for bookmark endpoints."""


from flask import request, flash, render_template, g, Blueprint
from webargs.flaskparser import use_args

from bookmarks.api.schemas import (
    BookmarksQueryArgsSchema
)
from ..models import Bookmark
from ..forms import AddBookmarkForm
from ..logic import _get

bookmarks = Blueprint('bookmarks', __name__)


@bookmarks.route('/bookmarks/')
@use_args(BookmarksQueryArgsSchema(), location='query')
def get(args):
    """Return all bookmarks with the tag name."""
    query = _get(args)
    pag = query.paginate(page=request.args.get('page', 1, type=int),
                         per_page=5)
    if g.user and g.user.is_authenticated:
        user_votes = g.user.votes.all()
        # FIXME can this be improved with one query?
        for bookmark in pag.items:
            for vote in user_votes:
                if bookmark.id == vote.bookmark_id:
                    bookmark.vote = vote
                    break
    return render_template('bookmarks/list_bookmarks.html',
                           form=AddBookmarkForm(),
                           paginator=pag, tag_name='all')


@bookmarks.route('/bookmarks/search')
def search():
    """Search bookmarks."""
    flash('Sorry, search is not implemented yet :(', 'info')
    pag = Bookmark.query.filter_by(id=None).paginate(
        page=request.args.get('page', 1, type=int), per_page=5)
    return render_template('bookmarks/list_bookmarks.html',
                           form=AddBookmarkForm(),
                           paginator=pag)
