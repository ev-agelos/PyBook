"""Define all views."""


from flask import flash, render_template, request
from flask.ext.login import login_required
from sqlalchemy import distinct
from app import app, db
from models import Bookmark
from forms import AddBookmark


@app.route('/')
def home():
    """Landing page."""
    categories = db.session.query(distinct(Bookmark.category))
    return render_template('index.html', categories=categories)


@app.route('/category/<option>')
def get_bookmarks(option):
    """Return bookmarks according to <option> category."""
    option = option.replace('_', ' ')
    bookmarks = Bookmark.query.filter_by(category=option)
    return render_template('list_bookmarks.html', title=option.capitalize(),
                           results=bookmarks)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_bookmark():
    """Add new bookmark to database."""
    form = AddBookmark(request.form)
    if form.validate_on_submit():
        if not form.category.data:
            form.category.data = 'uncategorized'
        existing_url = db.session.query(Bookmark).filter_by(url=form.url.data)
        if existing_url is None:
            new_bookmark = Bookmark(**form.data)
            db.session.add(new_bookmark)
            db.session.commit()
            flash("Added!")
        else:
            flash('Url already exists.')
    return render_template('add_bookmark.html', form=form)
