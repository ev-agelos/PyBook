"""This module contains the landing endpoint."""

from flask import request, Blueprint
from sqlalchemy.sql.expression import asc, desc

from bookmarks import db
from bookmarks.models import Bookmark
from .utils import custom_render


index = Blueprint('index', __name__)


@index.route('/')
@custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
def home():
    """Landing page with latest added bookmarks."""
    orders = {
        'new': desc(Bookmark.created_on), 'oldest': asc(Bookmark.created_on),
        'top': desc(Bookmark.rating), 'unpopular': asc(Bookmark.rating)}
    ordering_by = orders.get(request.args.get('order_by'), orders['new'])

    query = db.session.query(Bookmark).order_by(ordering_by)

    return (query, 'latest')
