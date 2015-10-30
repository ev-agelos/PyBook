"""This module contains the landing endpoint."""

from flask import g, render_template

from bookmarks_app import app, db
from bookmarks_app.models import Bookmark, User, Vote
from .utils import paginate


@app.route('/')
def home():
    """Landing page with latest added bookmarks."""
    if g.user.is_authenticated():
        latest_bookmarks = db.query(Bookmark, User, Vote).join(User).outerjoin(
            Vote, Vote.bookmark_id == Bookmark._id).order_by(
                Bookmark.created_on.desc())
    else:
        latest_bookmarks = db.query(Bookmark, User).join(User).order_by(
            Bookmark.created_on.desc())
    paginator = paginate(latest_bookmarks)
    return render_template('list_bookmarks.html', bookmarks=paginator,
                           category_name='latest')
