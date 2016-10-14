from flask import render_template
from flask_classy import FlaskView, route
from sqlalchemy import func

from bookmarks import db
from ..models import Category, Bookmark
from .utils import paginate


class CategoriesView(FlaskView):
    """Endpoints for categories resource."""

    def get(self):
        """Return categories."""
        query = db.session.query(
            Category.name, func.count(Bookmark.category_id)).filter(
                Bookmark.category_id == Category.id).group_by(Category.id)
        template = 'list_categories.html'
        return render_template('bookmarks/' + template,
                               paginator=paginate(query))
