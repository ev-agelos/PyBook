"""This module contains the landing endpoint."""

from flask import g, request, Blueprint
from sqlalchemy import and_
from sqlalchemy.sql.expression import asc, desc

from main import db
from bookmarks.models import Bookmark, Vote, SaveBookmark
from bookmarks.views.utils import custom_render, serialize_models

from auth.models import User


index = Blueprint('index', __name__)


@index.route('/')
@custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
def home():
    """Landing page with latest added bookmarks."""
    orders = {
        'new': desc(Bookmark.created_on), 'oldest': asc(Bookmark.created_on),
        'top': desc(Bookmark.rating), 'unpopular': asc(Bookmark.rating)}
    ordering_by = orders.get(request.args.get('order_by'), orders['new'])

    if g.user.is_authenticated:
        query = db.session.query(Bookmark, User).join(User).outerjoin(
            SaveBookmark, and_(
                SaveBookmark.bookmark_id == Bookmark._id,
                SaveBookmark.user_id == g.user._id)).outerjoin(Vote, and_(
                    Vote.bookmark_id == Bookmark._id,
                    Vote.user_id == g.user._id)).add_entity(
                        SaveBookmark).add_entity(Vote).order_by(ordering_by)
    else:
        query = db.session.query(Bookmark, User).join(User).order_by(
            ordering_by)

    bookmarks = serialize_models(query)
    return (bookmarks, 'latest')
