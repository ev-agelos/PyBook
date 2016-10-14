"""Views for bookmark endpoints."""


from flask import request, g, flash, redirect, url_for, jsonify
from flask_login import login_required
from flask_classy import FlaskView, route
from sqlalchemy.sql.expression import asc, desc
from werkzeug.exceptions import BadRequest, Forbidden

from bookmarks import db

from ..models import Bookmark, Category, Vote, SaveBookmark
from .utils import custom_render


class BookmarksView(FlaskView):
    """Endpoints for bookmarks resource."""

    sort = {
        'date': desc(Bookmark.created_on), '-date': asc(Bookmark.created_on),
        'rating': desc(Bookmark.rating), '-rating': asc(Bookmark.rating)
    }

    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def get(self):
        """Return all bookmarks with the category name."""
        query = db.session.query(Bookmark)
        if request.args.get('category'):
            category = Category.query.filter_by(
                name=request.args.get('category')).first()
            if category is not None:
                query = query.filter_by(category_id=category.id)

        if request.args.get('sort'):
            sort_args = request.args.get('sort', '').split(',')
            for sort in sort_args:
                if sort in self.sort:
                    query = query.order_by(self.sort[sort])
        else:  # sort newest as default sorting
            query = query.order_by(self.sort['date'])

        return (query, 'all')

    @route('/search')
    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def search(self):
        """Search bookmarks."""
        flash('Sorry, search is not implemented yet :(', 'info')
        return ([], 'all')


    @route('/<int:id>/vote', methods=['POST'])
    @login_required
    def vote_bookmark(self, id):
        """Vote up/down bookmark."""
        vote_direction = request.json.get('vote')
        if vote_direction not in (-1, 1):
            raise BadRequest
        bookmark = Bookmark.query.get_or_404(id)
        if bookmark.vote is None:
            vote = Vote(user_id=g.user.id, bookmark_id=bookmark.id,
                        direction=False if vote_direction == -1  else True)
            db.session.add(vote)
            bookmark.rating += vote_direction
        else:
            if vote_direction == 1:  # Positive vote
                if bookmark.vote.direction:
                    bookmark.vote.direction = None
                    bookmark.rating -= 1
                else:
                    if bookmark.vote.direction is None:
                        bookmark.rating += 1
                    else:
                        bookmark.rating += 2
                    bookmark.vote.direction = True
            else:  # Negative vote
                if bookmark.vote.direction == False:
                    bookmark.vote.direction = None
                    bookmark.rating += 1
                else:
                    if bookmark.vote.direction is None:
                        bookmark.rating -= 1
                    else:
                        bookmark.rating -= 2
                    bookmark.vote.direction = False
        try:
            db.session.add(bookmark)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return str(bookmark.rating)

    @login_required
    def delete(self, id):
        """Delete a bookmark."""
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            return jsonify({'message': 'not found'}), 404
        if bookmark.user_id != g.user.id:
            return jsonify({'message': 'forbidden'}), 403
        # Delete associated categories
        if Bookmark.query.filter_by(
                category_id=bookmark.category_id).count() == 1:
            category = Category.query.get(bookmark.category_id)
            db.session.delete(category)
        # Delete associated votes
        db.session.query(Vote).filter_by(bookmark_id=id).delete()
        # Delete associated saves
        db.session.query(SaveBookmark).filter_by(bookmark_id=id).delete()

        db.session.delete(bookmark)
        db.session.commit()

        return ('', 204)
