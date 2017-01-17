from flask import render_template, request, Blueprint
from sqlalchemy import func

from bookmarks import db
from ..models import Tag, Bookmark, tags_bookmarks


tags = Blueprint('tags', __name__)


@tags.route('/tags')
def get():
    """Return tags."""
    query = db.session.query(Tag.name, func.count(Tag.id)).join(
        tags_bookmarks).group_by(Tag.id).all()

    return render_template('bookmarks/list_tags.html', tags=query)
