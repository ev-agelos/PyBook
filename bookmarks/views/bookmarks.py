"""Define all views."""

import json
from urllib.parse import urlparse

from flask import flash, render_template, abort, request
from flask.ext.login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from werkzeug.exceptions import Forbidden, BadRequest
from werkzeug.utils import secure_filename

from bookmarks import app, db
from bookmarks.models import Bookmark, Category, Vote
from bookmarks.forms import AddBookmarkForm


@app.route('/categories')
@app.route('/')
def home():
    """Landing page."""
    categories = db.session.query(
        Category._id, Category.name, func.count(Bookmark.category_id)).filter(
            Bookmark.category_id == Category._id).group_by(Category._id).all()
    return render_template('list_categories.html', categories=categories)


@app.route('/bookmarks')
def get_bookmarks():
    """Return all bookmarks."""
    bookmarks = Bookmark.query.all()
    if current_user.is_authenticated():
        votes = Vote.query.filter_by(user_id=current_user._id)
        for bookmark in bookmarks:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    return render_template('list_bookmarks.html', bookmarks=bookmarks,
                           category_name='all')


@app.route('/categories/<int:category_id>')
def get_bookmarks_by_category(category_id):
    """Return the bookmarks according to category id passed."""
    category = Category.query.get(category_id)
    if not category:
        abort(404)
    bookmarks = Bookmark.query.filter_by(category_id=category_id).all()
    if current_user.is_authenticated():
        votes = Vote.query.filter_by(user_id=current_user._id)
        for bookmark in bookmarks:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    return render_template('list_bookmarks.html', category_name=category.name,
                           bookmarks=bookmarks)


@app.route('/users/<int:user_id>/categories')
def get_user_categories(user_id):
    """Return user's categories."""
    categories = db.session.query(
        Category._id, Category.name, func.count(Bookmark.category_id)).filter(
            Bookmark.category_id == Category._id,
            Bookmark.user_id == user_id).group_by(Category._id).all()
    return render_template('list_categories.html', categories=categories)


@app.route('/users/<int:user_id>/categories/<int:category_id>')
def get_user_bookmarks_by_category(user_id, category_id):
    """Return current user's bookmarks according to category id passed."""
    bookmarks = Bookmark.query.filter(
        Bookmark.user_id == user_id).filter_by(category_id=category_id).all()
    if not bookmarks:
        abort(404)
    if current_user.is_authenticated():
        votes = Vote.query.filter_by(user_id=current_user._id)
        for bookmark in bookmarks:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    category = Category.query.get(category_id)
    return render_template('list_bookmarks.html', category_name=category.name,
                           bookmarks=bookmarks)


@app.route('/users/<int:user_id>/bookmarks/<int:bookmark_id>')
def get_user_bookmark_by_id(user_id, bookmark_id):
    """Return user's bookmark according to ids passed."""
    try:
        bookmark = Bookmark.query.filter(
            Bookmark.user_id == user_id).filter_by(_id=bookmark_id).one()
    except NoResultFound:
        abort(404)
    category_name = Category.query.get(bookmark.category_id).name
    return render_template('list_bookmarks.html', category_name=category_name,
                           bookmarks=[bookmark])


@app.route('/users/<int:user_id>/bookmarks/')
def get_all_user_bookmarks(user_id):
    """Return all user's bookmarks."""
    bookmarks = Bookmark.query.filter_by(user_id=user_id)
    if current_user.is_authenticated():
        votes = Vote.query.filter_by(user_id=current_user._id)
        for bookmark in bookmarks:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    return render_template('list_bookmarks.html', category_name='all',
                           bookmarks=bookmarks)


@app.route('/users/<int:user_id>/bookmarks/<int:bookmark_id>/update',
           methods=['GET', 'POST'])
@login_required
def update_bookmark(user_id, bookmark_id):
    """Update existing bookmark."""
    if user_id != current_user._id:
        raise Forbidden
    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark.user_id != user_id:
        raise Forbidden
    category = Category.query.get(bookmark.category_id)
    form = AddBookmarkForm()
    if form.validate_on_submit():
        # Check first if url changed and exists in other user's bookmarks
        if form.url.data != bookmark.url and Bookmark.query.filter(
            Bookmark.user_id != current_user._id).filter_by(
                url=form.url.data).first():
            flash('Url already exists.')
        else:
            # If category changed and old one doesnt have any links delete it
            if form.category.data and category.name != form.category.data:
                if len(category.bookmarks) == 1:
                    db.session.delete(category)
                try:  # Check if new category already exists
                    category = Category.query.filter_by(
                        name=form.category.data).one()
                except NoResultFound:
                    category = Category(name=form.category.data)
                    db.session.add(category)
                    db.session.flush()
                    flash("New category added!")
                bookmark.category_id = category._id
            bookmark.title = form.title.data
            bookmark.url = form.url.data
            db.session.commit()
            flash("Bookmark Updated!")
    else:
        form = AddBookmarkForm(category=category.name,
                               title=bookmark.title,
                               url=bookmark.url)
    return render_template('add_bookmark.html', form=form)


@app.route('/users/<int:user_id>/bookmarks/add', methods=['GET', 'POST'])
@login_required
def add_bookmark(user_id):
    """Add new bookmark to database."""
    if user_id != current_user._id:
        raise Forbidden
    form = AddBookmarkForm()
    if form.validate_on_submit():
        try:
            Bookmark.query.filter_by(url=form.url.data).one()
            flash('Url already exists.')
        except NoResultFound:
            try:
                category = Category.query.filter_by(
                    name=form.data.get('category', 'Uncategorized')).one()
            except NoResultFound:
                category = Category(name=form.category.data)
                db.session.add(category)
                db.session.flush()
            bookmark = Bookmark(title=form.title.data, url=form.url.data,
                                category_id=category._id,
                                user_id=current_user._id)
            db.session.add(bookmark)
            db.session.commit()
            flash("Added!")
    return render_template('add_bookmark.html', form=form)


@app.route('/bookmarks/import', methods=['GET', 'POST'])
@login_required
def import_bookmarks():
    """Import bookmarks from file with json format."""
    if request.method == 'POST':
        filefile = request.files['file']
        if filefile:
            secure_filename(filefile.filename)
            data = filefile.read()
            try:
                decoded_data = data.decode('unicode_escape')
                json_data = json.loads(decoded_data)
                for category_name, value in json_data.items():
                    category = Category(name=category_name)
                    db.session.add(category)
                    db.session.flush()
                    db.session.refresh(category)
                    if isinstance(value, list):
                        for link in value:
                            bookmark = Bookmark(title=urlparse(link).netloc,
                                                url=link,
                                                category_id=category._id,
                                                user_id=current_user._id)
                            db.session.add(bookmark)
                    elif isinstance(value, dict):
                        for title, link in value.items():
                            bookmark = Bookmark(title=title, url=link,
                                                category_id=category._id,
                                                user_id=current_user._id)
                            db.session.add(bookmark)
                db.session.commit()
            except Exception as e:
                with open('my_error_log.txt') as fob:
                    fob.write(str(e))
    return render_template('import_bookmarks.html')


@app.route('/bookmarks/<int:bookmark_id>/vote', methods=['POST'])
@login_required
def vote_bookmark(bookmark_id):
    """Vote up/down bookmark."""
    vote_direction = request.json.get('vote')
    if vote_direction not in range(-1, 2):
        raise BadRequest
    values = {-1: False, 0: None, 1: True}
    change = vote_direction
    try:
        vote = Vote.query.filter_by(user_id=current_user._id,
                                    bookmark_id=bookmark_id).one()
        if vote.direction is not None and vote_direction:
            vote.direction = values[-vote_direction]
            change = -2 * vote_direction
        elif vote.direction is None and vote_direction:
            # From no rating, add the new one
            vote.direction = values[vote_direction]
            change = vote_direction
        else:
            # Revert back from -1 or +1 to 0
            if not vote.direction:
                change = 1
            else:
                change = -1
            vote.direction = values[vote_direction]

    except NoResultFound:
        vote = Vote(direction=values[vote_direction], user_id=current_user._id,
                    bookmark_id=bookmark_id)
    try:
        bookmark = Bookmark.query.filter(Bookmark.user_id != current_user._id,
                                         Bookmark._id == bookmark_id).one()
    except NoResultFound:
        abort(404)
    bookmark.rating += change
    db.session.add_all([vote, bookmark])
    db.session.commit()
    return str(bookmark.rating)
