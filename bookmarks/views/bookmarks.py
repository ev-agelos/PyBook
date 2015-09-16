"""Define all views."""


from flask import flash, render_template, request, abort
from flask.ext.login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Forbidden

from bookmarks import app, db
from bookmarks.models import Bookmark, Category
from bookmarks.forms import AddBookmarkForm


@app.route('/')
def home():
    """Landing page."""
    categories_query = db.session.query(Category).all()
    categories = [('/categories/' + str(category._id),
                  category.name.replace(' ', '_'))
                  for category in categories_query]
    return render_template('list_categories.html', categories=categories)


@app.route('/categories/<int:category_id>')
def get_bookmarks_by_category(category_id):
    """Return the bookmarks according to category id passed."""
    category = Category.query.get(category_id)
    if category:
        category_name = category.name
        bookmarks = Bookmark.query.filter_by(category_id=category_id).all()
        return render_template('list_bookmarks.html',
                               category_name=category_name,
                               bookmarks=bookmarks)
    else:
        abort(404)


@app.route('/categories/')
def get_categories():
    """Return all the categories."""
    categories_query = Category.query.all()
    categories = [(category._id, category.name.replace(' ', '_'))
                  for category in categories_query]
    return render_template('list_categories.html', categories=categories)


@app.route('/users/<int:user_id>/categories/')
@login_required
def get_user_categories(user_id, category_id=None):
    """Return user's categories."""
    if user_id != current_user._id:
        raise Forbidden
    categories = [(bookmark.category_id, bookmark.category.name)
                  for bookmark in current_user.bookmarks]
    return render_template('list_categories.html', categories=set(categories))


@app.route('/users/<int:user_id>/categories/<int:category_id>')
@login_required
def get_user_bookmarks_by_category(user_id, category_id):
    """Return current user's bookmarks according to category id passed."""
    if user_id != current_user._id:
        raise Forbidden
    for bookmark in current_user.bookmarks:
        if bookmark.category_id == category_id:
            category_name = bookmark.category.name
            break
    else:
        abort(404)
    bookmarks = [bookmark for bookmark in current_user.bookmarks
                 if bookmark.category_id == category_id]
    return render_template('list_bookmarks.html', category_name=category_name,
                           bookmarks=bookmarks)


@app.route('/users/<int:user_id>/bookmarks/<int:bookmark_id>')
@login_required
def get_user_bookmark_by_id(user_id, bookmark_id):
    """Return user's bookmark according to id passed."""
    if user_id != current_user._id:
        raise Forbidden
    for bookmark in current_user.bookmarks:
        if bookmark._id == bookmark_id:
            bookmarks = [bookmark]
            category_name = bookmark.category.name
            break
    else:
        abort(404)
    return render_template('list_bookmarks.html', category_name=category_name,
                           bookmarks=bookmarks)


@app.route('/users/<int:user_id>/bookmarks')
@login_required
def get_all_user_bookmarks(user_id):
    """Return all user's bookmarks."""
    if user_id != current_user._id:
        raise Forbidden
    bookmarks = [item for item in current_user.bookmarks]
    return render_template('list_bookmarks.html', category_name='all',
                           bookmarks=bookmarks)


@app.route('/users/<int:user_id>/categories/update')
@app.route('/users/<int:user_id>/categories/<int:category_id>/update',
           methods=['GET', 'POST'])
@app.route('/users/<int:user_id>/categories/<int:category_id>'
           '/bookmarks/<int:bookmark_id>/update', methods=['GET', 'POST'])
@login_required
def update_bookmark(user_id=None, category_id=None, bookmark_id=None):
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
                    bookmark.url = 'bookmarks/' + str(bookmark._id) + '/update'
                return render_template('list_bookmarks.html',
                                       category_name=category_name,
                                       bookmarks=bookmarks)
        else:
            categories = [('{}/update'.format(bookmark.category_id),
                           Category.query.get(
                            bookmark.category_id).name.replace(' ', '_'))
                          for bookmark in current_user.bookmarks]
            return render_template('list_categories.html',
                                   categories=set(categories))
    return render_template('edit_bookmark.html', form=form,
                           category=category_id,
                           bookmark_id=bookmark_id)


@app.route('/users/<int:user_id>/bookmarks/add', methods=['GET', 'POST'])
@login_required
def add_bookmark(user_id):
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
