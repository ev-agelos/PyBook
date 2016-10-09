from flask import render_template
from flask_classy import FlaskView, route
from sqlalchemy import func

from bookmarks import db
from ..models import Category, Bookmark
from .utils import paginate


class CategoriesView(FlaskView):
    """Endpoints for categories resource."""

    @route('/')
    @route('/<name>')
    def get(self, name=None):
        """Return categories."""
        if name is None:
            query = db.session.query(
                Category.name, func.count(Bookmark.category_id)).filter(
                    Bookmark.category_id == Category.id).group_by(Category.id)
            template = 'list_categories.html'
        else:
            category = Category.query.filter_by(name=name).first_or_404()
            query = db.session.query(Bookmark).filter(
                Bookmark.category_id == category.id)
            template = 'list_bookmarks.html'
        bookmarks = paginate(query)
        return render_template('bookmarks/' + template, paginator=bookmarks,
                               category_name=name)
