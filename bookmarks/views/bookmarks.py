"""Views for bookmark endpoints."""


from flask import request, g, flash, jsonify, render_template
from flask_login import login_required
from flask_classy import FlaskView, route
from sqlalchemy.sql.expression import asc, desc
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from bookmarks import db, csrf

from ..models import Bookmark, Category, Vote, Favourite
from ..forms import AddBookmarkForm
from .utils import custom_render, get_url_thumbnail


class BookmarksView(FlaskView):
    """Endpoints for bookmarks resource."""

    sort = {
        'date': desc(Bookmark.created_on), '-date': asc(Bookmark.created_on),
        'rating': desc(Bookmark.rating), '-rating': asc(Bookmark.rating)
    }

    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def index(self):
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

    @custom_render('bookmarks/list_bookmarks.html', check_thumbnails=True)
    def get(self, id):
        """Return a bookmark."""
        bookmark = Bookmark.query.get_or_404(id)
        category = Category.query.get(bookmark.category_id)
        return ([bookmark], category.name)

    @login_required
    def post(self):
        """Add new bookmark and add it's category if does not exist."""
        form = AddBookmarkForm()
        if form.validate():
            category_ = form.category.data.lower() or 'uncategorized'
            try:
                Bookmark.query.filter_by(url=form.url.data).one()
                status = 409
            except NoResultFound:
                try:
                    category = Category.query.filter_by(name=category_).one()
                except NoResultFound:
                    category = Category(name=category_)
                bookmark = Bookmark(title=form.title.data, url=form.url.data,
                                    user_id=g.user.id, category=category,
                                    image=get_url_thumbnail(form.url.data))
                db.session.add(bookmark)
                db.session.commit()
                status = 201
        else:
            status = 400
        return jsonify(form.data), status

    @login_required
    def put(self, id):
        """
        Update a bookmark entry.

        In case category changes check if no other bookmark is related with
        that category and if not, delete it.
        """
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            return jsonify({'message': 'Bookmark was not found'}), 404

        form = AddBookmarkForm()
        if not form.validate():
            return jsonify({'message': 'Invalid form'}), 400

        if form.url.data != bookmark.url:
            try:  # Check if url already exists
                Bookmark.query.filter_by(url=form.url.data).one()
                return jsonify({'message': 'Url already exists'}), 400
            except NoResultFound:
                pass

        category = Category.query.get(bookmark.category_id)
        if form.category.data.lower() != category.name:
            try:
                Category.query.filter_by(name=form.category.data.lower()).one()
            except NoResultFound:
                # Delete old category if no bookmarks are related with
                if category.bookmarks.count() == 1:
                    db.session.delete(category)
                bookmark.category = Category(name=form.category.data.lower())

        bookmark.title = form.title.data
        bookmark.url = form.url.data
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({'message': 'Bookmark updated'}), 200

    @route('/add')
    @login_required
    def add(self):
        """Return form for adding new bookmark."""
        form = AddBookmarkForm()
        category_list = db.session.query(Category).all()
        return render_template('bookmarks/add.html', form=form,
                               category_list=category_list)

    @route('/<int:id>/update')
    @login_required
    def update(self, id):
        """Return form for updating a bookmark."""
        bookmark = Bookmark.query.get_or_404(id)
        category = Category.query.get(bookmark.category_id)
        categories = db.session.query(Category).all()
        form = AddBookmarkForm(category=category.name, title=bookmark.title,
                               url=bookmark.url)
        return render_template('bookmarks/update.html', bookmark_id=id,
                               form=form, category_list=categories)

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
        db.session.query(Favourite).filter_by(user_id=g.user.id,
                                              bookmark_id=id).delete()

        db.session.delete(bookmark)
        db.session.commit()

        return ('', 204)

    @csrf.exempt
    @route('/<int:id>/save', methods=['PUT'])
    @login_required
    def save(self, id):
        """Favourite a bookmark."""
        if Bookmark.query.get(id) is None:
            return jsonify({'message': 'not found'}), 404

        message = 'saved'
        try:
            save = Favourite.query.filter_by(user_id=g.user.id,
                                             bookmark_id=id).one()
        except NoResultFound:
            save = Favourite(user_id=g.user.id, bookmark_id=id)
            status = 201
        else:
            if save.is_saved:
                message = 'unsaved'
            save.is_saved = not save.is_saved
            status = 200
        db.session.add(save)
        db.session.commit()

        return jsonify({'message': message}), status
