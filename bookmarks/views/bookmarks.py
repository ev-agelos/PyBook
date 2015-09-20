"""Define all views."""

import json
from urllib.parse import urlparse

from flask import flash, render_template, abort, request
from flask.ext.login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from werkzeug.exceptions import Forbidden
from werkzeug.utils import secure_filename

from bookmarks import app, db
from bookmarks.models import Bookmark, Category
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
    return render_template('list_bookmarks.html', bookmarks=bookmarks,
                           category_name='all')


@app.route('/categories/<int:category_id>')
def get_bookmarks_by_category(category_id):
    """Return the bookmarks according to category id passed."""
    category = Category.query.get(category_id)
    if not category:
        abort(404)
    bookmarks = Bookmark.query.filter_by(category_id=category_id).all()
    return render_template('list_bookmarks.html', category_name=category.name,
                            bookmarks=bookmarks)


@app.route('/users/<int:user_id>/categories')
@login_required
def get_user_categories(user_id, category_id=None):
    """Return user's categories."""
    if user_id != current_user._id:
        raise Forbidden
    categories = db.session.query(
        Category._id, Category.name, func.count(Bookmark.category_id)).filter(
            Bookmark.category_id == Category._id,
            Bookmark.user_id == user_id).group_by(Category._id).all()
    return render_template('list_categories.html', categories=categories)


@app.route('/users/<int:user_id>/categories/<int:category_id>')
@login_required
def get_user_bookmarks_by_category(user_id, category_id):
    """Return current user's bookmarks according to category id passed."""
    if user_id != current_user._id:
        raise Forbidden
    category = Category.query.get(category_id)
    if not category:
        abort(404)
    user_bookmarks = [bookmark for bookmark in current_user.bookmarks]
    bookmarks = [bookmark for bookmark in user_bookmarks
                 if bookmark.category_id == category_id]
    return render_template('list_bookmarks.html', category_name=category.name,
                           bookmarks=bookmarks)


@app.route('/users/<int:user_id>/bookmarks/<int:bookmark_id>')
@login_required
def get_user_bookmark_by_id(user_id, bookmark_id):
    """Return user's bookmark according to id passed."""
    if user_id != current_user._id:
        raise Forbidden
    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark.user_id != user_id:
        abort(404)
    category_name = Category.query.get(bookmark.category_id).name
    return render_template('list_bookmarks.html', category_name=category_name,
                           bookmarks=[bookmark])


@app.route('/users/<int:user_id>/bookmarks')
@login_required
def get_all_user_bookmarks(user_id):
    """Return all user's bookmarks."""
    if user_id != current_user._id:
        raise Forbidden
    bookmarks = [item for item in current_user.bookmarks]
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
        import ipdb;ipdb.set_trace()
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
            filename = secure_filename(filefile.filename)
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
                print(e)
    return render_template('import_bookmarks.html')
