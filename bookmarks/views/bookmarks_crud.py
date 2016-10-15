"""CRUD endpoints for bookmarks."""

import json
from urllib.parse import urlparse

from flask import render_template, flash, request, g, Blueprint, jsonify
from flask_login import login_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from bookmarks import db, csrf

from ..models import Category, Bookmark, SaveBookmark
from ..forms import AddBookmarkForm
from .utils import get_url_thumbnail


crud = Blueprint('crud', __name__)

@crud.route('/bookmarks/add', methods=['GET', 'POST'])
@login_required
def add_bookmark():
    """Add new bookmark to database."""
    form = AddBookmarkForm()
    category_list = db.session.query(Category).all()
    if form.validate_on_submit():
        try:
            db.session.query(Bookmark).filter_by(url=form.url.data).one()
            flash('Url already exists.', 'warning')
        except NoResultFound:
            img_name = get_url_thumbnail(form.url.data)
            if img_name is None:
                img_name = 'default.png'
            try:
                category = db.session.query(Category).filter_by(
                    name=form.data.get('category',
                                       'uncategorized').lower()).one()
            except NoResultFound:
                category = Category(name=form.category.data.lower())
                db.session.add(category)
                db.session.flush()
            bookmark = Bookmark(title=form.title.data, url=form.url.data,
                                image=img_name, category_id=category.id,
                                user_id=g.user.id)
            db.session.add(bookmark)
            db.session.commit()
            flash('Added!', 'success')
    return render_template('bookmarks/add_bookmark.html', form=form,
                           category_list=category_list)


@crud.route('/bookmarks/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_bookmark(id=None):
    """Update existing bookmark."""
    bookmark = Bookmark.query.get_or_404(id)

    category = db.session.query(Category).get(bookmark.category_id)
    category_list = db.session.query(Category).all()
    form = AddBookmarkForm()
    if form.validate_on_submit():
        # Check first if url changed and exists in other user's bookmarks
        if form.url.data != bookmark.url and db.session.query(Bookmark).filter(
                Bookmark.user_id != g.user.id).filter_by(
                    url=form.url.data).first():
            flash('Url already exists.', 'warning')
        else:
            # If category changed and old one doesn't have any links delete it
            if form.category.data and \
                    category.name != form.category.data.lower():
                if db.session.query(Bookmark).filter_by(
                        category_id=category.id).count() == 1:
                    db.session.delete(category)
                try:  # Check if new category already exists
                    category = db.session.query(Category).filter_by(
                        name=form.category.data.lower()).one()
                except NoResultFound:
                    category = Category(name=form.category.data.lower())
                    db.session.add(category)
                    db.session.flush()
                    flash('New category added!', 'success')
                bookmark.category_id = category.id
            bookmark.title = form.title.data
            bookmark.url = form.url.data
            db.session.commit()
            flash('Bookmark Updated!', 'success')
    else:
        form = AddBookmarkForm(category=category.name,
                               title=bookmark.title,
                               url=bookmark.url)
    return render_template('bookmarks/add_bookmark.html', form=form,
                           category_list=category_list)


@crud.route('/bookmarks/import', methods=['GET', 'POST'])
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
                    category = Category(name=category_name.lower())
                    db.session.add(category)
                    db.session.flush()
                    db.session.refresh(category)
                    if isinstance(value, list):
                        for link in value:
                            bookmark = Bookmark(
                                title=urlparse(link).netloc, url=link,
                                category_id=category.id, user_id=g.user.id)
                            db.session.add(bookmark)
                    elif isinstance(value, dict):
                        for title, link in value.items():
                            bookmark = Bookmark(title=title, url=link,
                                                category_id=category.id,
                                                user_id=g.user.id)
                            db.session.add(bookmark)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                with open('my_error_log.txt') as fob:
                    fob.write(str(e))
    return render_template('bookmarks/import_bookmarks.html')


@csrf.exempt
@crud.route('/bookmarks/<int:id>/save', methods=['PUT'])
@login_required
def save_bookmark(id):
    """Favourite a bookmark."""
    if Bookmark.query.get(id) is None:
        return jsonify({'message': 'not found'}), 404

    message = 'saved'
    try:
        save = SaveBookmark.query.filter_by(user_id=g.user.id,
                                            bookmark_id=id).one()
    except NoResultFound:
        save = SaveBookmark(user_id=g.user.id, bookmark_id=id)
        status = 201
    else:
        if save.is_saved:
            message = 'unsaved'
        save.is_saved = not save.is_saved
        status = 200
    db.session.add(save)
    db.session.commit()

    return jsonify({'message': message}), status
