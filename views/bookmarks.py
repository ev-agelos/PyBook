"""Define all views."""


from flask import flash, render_template, request
from flask.ext.login import login_required, current_user
from sqlalchemy import distinct
from sqlalchemy.orm.exc import NoResultFound

from app import app, db
from models import Bookmark
from forms import AddBookmarkForm


@app.route('/')
def home():
    """Landing page."""
    categories_query = db.session.query(distinct(Bookmark.category))
    categories = [category[0] for category in categories_query]
    return render_template('index.html', categories=categories)


@app.route('/category/<option>')
def get_bookmarks(option):
    """Return bookmarks according to <option> category."""
    option = option.replace('_', ' ')
    bookmarks = Bookmark.query.filter_by(category=option)
    return render_template('list_bookmarks.html', title=option.capitalize(),
                           results=bookmarks)


@app.route('/my_bookmarks')
@login_required
def get_my_bookmarks():
    """Return current user's bookmarks."""
    categories = [bookmark.category for bookmark in current_user.bookmarks]
    return render_template('index.html', categories=categories)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_bookmark():
    """Add new bookmark to database."""
    form = AddBookmarkForm(request.form)
    if form.validate_on_submit():
        if not form.category.data:
            form.category.data = 'uncategorized'
        try:
            db.session.query(Bookmark).filter_by(url=form.url.data).one()
            flash('Url already exists.')
        except NoResultFound:
            new_bookmark = Bookmark(user_id=current_user._id, **form.data)
            db.session.add(new_bookmark)
            db.session.commit()
            flash("Added!")
    return render_template('add_bookmark.html', form=form)
