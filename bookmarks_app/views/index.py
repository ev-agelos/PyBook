"""This module contains the landing endpoint."""

from flask import g, render_template, request
from sqlalchemy.sql.expression import asc, desc

from bookmarks_app import app, db
from bookmarks_app.models import Bookmark, User, Vote
from .utils import render_it, serialize_models


@app.route('/')
@render_it('list_bookmarks.html', check_thumbnails=True)
def home():
    """Landing page with latest added bookmarks."""
    orders = {
        'new': desc(Bookmark.created_on), 'oldest': asc(Bookmark.created_on),
        'top': desc(Bookmark.rating), 'unpopular': asc(Bookmark.rating)}
    ordering_by = orders.get(request.args.get('order_by'), orders['new'])

    if g.user.is_authenticated():
        query = db.query(Bookmark, User, Vote).join(User).outerjoin(
            Vote, Vote.bookmark_id == Bookmark._id).order_by(ordering_by)
    else:
        query = db.query(Bookmark, User).join(User).order_by(ordering_by)

    bookmarks = serialize_models(query)
    return (bookmarks, 'latest')
