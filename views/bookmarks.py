"""Define all views."""


from flask import flash, render_template, request
from flask.ext.login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound

from app import app, db
from models import Bookmark, Category
from forms import AddBookmarkForm


@app.route('/')
def home():
    """Landing page."""
    categories_query = db.session.query(Category).all()
    categories = [('/category/' + str(category._id),
                  category.name.replace(' ', '_'))
                  for category in categories_query]
    return render_template('index.html', categories=categories)


@app.route('/category/<int:category_id>')
def get_bookmarks_by_category(category_id):
    """Return bookmarks according to category id."""
    category = Category.query.get(category_id)
    if category:
        category_name = category.name.capitalize()
        bookmarks = db.session.query(Bookmark).filter_by(
            category_id=category_id).all()
    else:
        category_name = ''.capitalize()
        bookmarks = []
    return render_template('list_bookmarks.html', title=category_name,
                           results=bookmarks)


@app.route('/my_bookmarks')
@login_required
def get_my_categories():
    """Return current user's bookmarks."""
    categories = [('/category/' + str(bookmark.category_id),
                  bookmark.category.name)
                  for bookmark in current_user.bookmarks]
    return render_template('index.html', categories=set(categories))


@app.route('/update')
@app.route('/update/<int:category_id>', methods=['GET', 'POST'])
@app.route('/update/<int:category_id>/<int:bookmark_id>',
           methods=['GET', 'POST'])
@login_required
def update_bookmark(category_id=None, bookmark_id=None):
    """Update current user's bookmarks."""
    form = AddBookmarkForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if db.session.query(Bookmark).filter(
                Bookmark.user_id != current_user._id).filter_by(
                    url=form.url.data).first():
                flash('Url already exists.')
            else:
                category = Category.query.get(category_id)
                category.name = form.data.get('category', 'Uncategorized')
                bookmark = Bookmark.query.get(bookmark_id)
                bookmark.title = form.title.data
                bookmark.url = form.url.data
                db.session.commit()
                flash("Bookmark Updated!")
    elif request.method == 'GET':
        if category_id:
            category_name = Category.query.get(category_id).name
            if bookmark_id:
                for item in current_user.bookmarks:
                    if item._id == bookmark_id:
                        bookmark = item
                        form = AddBookmarkForm(category=category_name,
                                               title=bookmark.title,
                                               url=bookmark.url)
                        break
            else:
                bookmarks = [bookmark for bookmark in current_user.bookmarks
                             if bookmark.category_id == category_id]
                for bookmark in bookmarks:
                    bookmark.url = str(category_id) + '/' + str(bookmark._id)
                return render_template('list_bookmarks.html',
                                       title=category_name.capitalize(),
                                       results=bookmarks)
        else:
            categories = [('/update/' + str(bookmark.category_id),
                           Category.query.get(
                            bookmark.category_id).name.replace(' ', '_'))
                          for bookmark in current_user.bookmarks]
            return render_template('index.html', categories=set(categories))
    return render_template('edit_bookmark.html', form=form,
                           category=category_id,
                           bookmark_id=bookmark_id)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_bookmark():
    """Add new bookmark to database."""
    form = AddBookmarkForm(request.form)
    if form.validate_on_submit():
        form.category.data = form.data.get('category', 'Uncategorized')
        try:
            db.session.query(Bookmark).filter_by(url=form.url.data).one()
            flash('Url already exists.')
        except NoResultFound:
            category = db.session.query(Category).filter_by(
                name=form.category.data).first()
            if not category:
                category = Category(name=form.category.data)
                db.session.add(category)
                db.session.flush()
                db.session.refresh(category)
            bookmark = Bookmark(title=form.title.data, url=form.url.data,
                                category_id=category._id,
                                user_id=current_user._id)
            db.session.add(bookmark)
            db.session.commit()
            flash("Added!")
    return render_template('add_bookmark.html', form=form)
