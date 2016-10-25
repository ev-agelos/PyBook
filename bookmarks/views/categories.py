from flask import render_template, request, Blueprint
from sqlalchemy import func

from bookmarks import db
from ..models import Category, Bookmark


categories = Blueprint('categories', __name__)


@categories.route('/categories')
def get():
    """Return categories."""
    query = db.session.query(
        Category.name, func.count(Bookmark.category_id)).filter(
            Bookmark.category_id == Category.id).group_by(Category.id).all()

    return render_template('bookmarks/list_categories.html', categories=query)
