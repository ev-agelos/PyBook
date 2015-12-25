"""This module contains the landing endpoint."""

from flask import g, render_template

from bookmarks_app import app, db
from bookmarks_app.models import Bookmark, User, Vote
from .utils import render_it, serialize_models


@app.route('/')
@render_it('list_bookmarks.html', check_thumbnails=True)
def home():
    """Landing page with latest added bookmarks."""
    if g.user.is_authenticated():
        query = db.query(Bookmark, User, Vote).join(User).outerjoin(
            Vote, Vote.bookmark_id == Bookmark._id).order_by(
                Bookmark.created_on.desc())
    else:
        query = db.query(Bookmark, User).join(User).order_by(
            Bookmark.created_on.desc())
    bookmarks = serialize_models(query)
    return (bookmarks, 'latest')
