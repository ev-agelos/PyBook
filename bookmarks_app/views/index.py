"""This module contains the landing endpoint."""

from flask import g, render_template, request
from sqlalchemy import and_
from sqlalchemy.sql.expression import asc, desc

from bookmarks_app import app, db
from bookmarks_app.models import Bookmark, User, Vote, SaveBookmark
from .bookmark_views.utils import custom_render, serialize_models


@app.route('/')
@custom_render('list_bookmarks.html', check_thumbnails=True)
def home():
    """Landing page with latest added bookmarks."""
    orders = {
        'new': desc(Bookmark.created_on), 'oldest': asc(Bookmark.created_on),
        'top': desc(Bookmark.rating), 'unpopular': asc(Bookmark.rating)}
    ordering_by = orders.get(request.args.get('order_by'), orders['new'])

    if g.user.is_authenticated():
        query = db.query(Bookmark, User).join(User).outerjoin(
            SaveBookmark, and_(
                SaveBookmark.bookmark_id == Bookmark._id,
                SaveBookmark.user_id == g.user._id)).outerjoin(Vote, and_(
                    Vote.bookmark_id == Bookmark._id,
                    Vote.user_id == g.user._id)).add_entity(
                        SaveBookmark).add_entity(Vote).order_by(ordering_by)
    else:
        query = db.query(Bookmark, User).join(User).order_by(ordering_by)

    bookmarks = serialize_models(query)
    return (bookmarks, 'latest')
