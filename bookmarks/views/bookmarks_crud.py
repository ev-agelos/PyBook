"""CRUD endpoints for bookmarks."""

import json
from urllib.parse import urlparse

from flask import render_template, flash, abort, request, g
from flask_login import login_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename
from werkzeug.exceptions import Forbidden

from bookmarks import app, db
from bookmarks.models import Category, Bookmark
from bookmarks.forms import AddBookmarkForm


@app.route('/users/<username>/bookmarks/add', methods=['GET', 'POST'])
@login_required
def add_bookmark(username):
    """Add new bookmark to database."""
    if username != g.user.username:
        raise Forbidden
    form = AddBookmarkForm()
    if form.validate_on_submit():
        try:
            db.query(Bookmark).filter_by(url=form.url.data).one()
            flash('Url already exists.')
        except NoResultFound:
            try:
                category = db.query(Category).filter_by(
                    name=form.data.get('category', 'Uncategorized')).one()
            except NoResultFound:
                category = Category(name=form.category.data)
                db.add(category)
                db.flush()
            bookmark = Bookmark(title=form.title.data, url=form.url.data,
                                category_id=category._id, user_id=g.user._id)
            db.add(bookmark)
            db.commit()
            flash("Added!")
    return render_template('add_bookmark.html', form=form)


@app.route('/bookmarks/<title>/update', methods=['GET', 'POST'])
@login_required
def update_bookmark(title):
    """Update existing bookmark."""
    try:
        bookmark = db.query(Bookmark).filter(Bookmark.title == title).one()
    except NoResultFound:
        abort(404)
    if bookmark.user_id != g.user._id:
        raise Forbidden

    category = db.query(Category).get(bookmark.category_id)
    form = AddBookmarkForm()
    if form.validate_on_submit():
        # Check first if url changed and exists in other user's bookmarks
        if form.url.data != bookmark.url and db.query(Bookmark).filter(
                Bookmark.user_id != g.user._id).filter_by(
                    url=form.url.data).first():
            flash('Url already exists.')
        else:
            # If category changed and old one doesn't have any links delete it
            if form.category.data and category.name != form.category.data:
                if db.query(Category).filter_by(
                        name=category.name).count() == 1:
                    db.delete(category)
                try:  # Check if new category already exists
                    category = db.query(Category).filter_by(
                        name=form.category.data).one()
                except NoResultFound:
                    category = Category(name=form.category.data)
                    db.add(category)
                    db.flush()
                    flash("New category added!")
                bookmark.category_id = category._id
            bookmark.title = form.title.data
            bookmark.url = form.url.data
            db.commit()
            flash("Bookmark Updated!")
    else:
        form = AddBookmarkForm(category=category.name,
                               title=bookmark.title,
                               url=bookmark.url)
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
                    db.add(category)
                    db.flush()
                    db.refresh(category)
                    if isinstance(value, list):
                        for link in value:
                            bookmark = Bookmark(
                                title=urlparse(link).netloc, url=link,
                                category_id=category._id, user_id=g.user._id)
                            db.add(bookmark)
                    elif isinstance(value, dict):
                        for title, link in value.items():
                            bookmark = Bookmark(title=title, url=link,
                                                category_id=category._id,
                                                user_id=g.user._id)
                            db.add(bookmark)
                db.commit()
            except Exception as e:
                db.rollback()
                with open('my_error_log.txt') as fob:
                    fob.write(str(e))
    return render_template('import_bookmarks.html')
