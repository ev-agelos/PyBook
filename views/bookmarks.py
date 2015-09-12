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
    categories = [('/category/' + category[0].replace(' ', '_'), category[0])
                  for category in categories_query]
    return render_template('index.html', categories=categories)


@app.route('/category/<option>')
def get_categories(option):
    """Return bookmarks according to <option> category."""
    option = option.replace('_', ' ')
    bookmarks = Bookmark.query.filter_by(category=option)
    return render_template('list_bookmarks.html', title=option.capitalize(),
                           results=bookmarks)


@app.route('/my_bookmarks')
@login_required
def get_my_categories():
    """Return current user's bookmarks."""
    categories = [('/category/' + bookmark.category, bookmark.category)
                  for bookmark in current_user.bookmarks]
    return render_template('index.html', categories=categories)


@app.route('/update')
@app.route('/update/<input_category>', methods=['GET', 'POST'])
@app.route('/update/<input_category>/<int:bookmark_id>',
           methods=['GET', 'POST'])
@login_required
def update_bookmark(input_category=None, bookmark_id=None):
    """Update current user's bookmarks."""
    form = AddBookmarkForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if db.session.query(Bookmark).filter(
                Bookmark.user_id != current_user._id).filter_by(
                    url=form.url.data).first():
                flash('Url already exists.')
            else:
                bookmark = Bookmark.query.get(bookmark_id)
                bookmark.category = form.category.data
                bookmark.title = form.title.data
                bookmark.url = form.url.data
                db.session.commit()
                flash("Bookmark Updated!")
    elif request.method == 'GET':
        if input_category and bookmark_id:
            row = Bookmark.query.get(int(bookmark_id))
            form = AddBookmarkForm(category=row.category, title=row.title,
                                   url=row.url)
        elif input_category:
            input_category = input_category.replace('_', ' ')
            bookmarks = db.session.query(Bookmark).filter_by(
                category=input_category, user_id=current_user._id)
            for item in bookmarks:
                item.url = input_category + '/' + str(item._id)
            return render_template('list_bookmarks.html',
                                   title=input_category.capitalize(),
                                   results=bookmarks)
        else:
            categories = db.session.query(distinct(
                Bookmark.category)).filter_by(user_id=current_user._id)
            categories = [('/update/' + category[0].replace(' ', '_'),
                          category[0])
                          for category in categories]
            return render_template('index.html', categories=categories)
    return render_template('edit_bookmark.html', form=form,
                           category=input_category,
                           bookmark_id=bookmark_id)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_bookmark():
    """Add new bookmark to database."""
    form = AddBookmarkForm(request.form)
    if form.validate_on_submit():
        form.category.data = form.data.get('category', 'uncategorized')
        try:
            db.session.query(Bookmark).filter_by(url=form.url.data).one()
            flash('Url already exists.')
        except NoResultFound:
            new_bookmark = Bookmark(user_id=current_user._id, **form.data)
            db.session.add(new_bookmark)
            db.session.commit()
            flash("Added!")
    return render_template('add_bookmark.html', form=form)
