"""Views for bookmark endpoints."""

import json
from urllib.parse import urlparse

from flask import flash, render_template, abort, request, g
from flask.ext.login import login_required, current_user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from werkzeug.exceptions import Forbidden, BadRequest
from werkzeug.utils import secure_filename

from bookmarks import app, db
from bookmarks.models import Bookmark, Category, Vote, User
from bookmarks.forms import AddBookmarkForm


@app.route('/')
@app.route('/categories')
def home():
    """Show all categories."""
    paginator = db.query(
        Category.name, func.count(Bookmark.category_id)).filter(
            Bookmark.category_id == Category._id).group_by(
                Category._id).paginate(page=request.args.get('page', 1),
                                       per_page=5)
    return render_template('list_categories.html', categories=paginator,
                           category_name='latest')


@app.route('/bookmarks/')
def get_bookmarks():
    """
    Return Pagination object with all Bookmarks and their Users.

    Return 5 bookmarks per page. Join username to each bookmark.
    If user is logged in get the votes to show colored vote up/down(if voted).
    """
    paginator = db.query(Bookmark, User).join(User).paginate(
        request.args.get('page', 1), per_page=5)
    if current_user.is_authenticated():
        votes = db.query(Vote).filter_by(
            user_id=current_user._id).all()
        for bookmark, _ in paginator.items:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    return render_template('list_bookmarks.html', bookmarks=paginator,
                           category_name='all')


@app.route('/categories/<name>')
def get_bookmarks_by_category(name):
    """Return the bookmarks according to category id passed."""
    try:
        category = db.query(Category).filter_by(name=name).one()
    except NoResultFound:
        abort(404)
    bookmarks_users = db.query(Bookmark, User).filter(
        Bookmark.category_id == category._id).join(User).paginate(
            page=request.args.get('page', 1), per_page=5)
    if current_user.is_authenticated():
        votes = db.query(Vote).filter_by(
            user_id=current_user._id).all()
        for bookmark, _ in bookmarks_users:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    return render_template('list_bookmarks.html', category_name=name,
                           bookmarks=bookmarks_users)


@app.route('/users/<username>/categories')
def get_categories_by_user(username):
    """Return user's categories."""
    try:
        user = db.query(User).filter_by(username=username).one()
    except NoResultFound:
        abort(404)
    categories = db.query(
        Category.name, func.count(Bookmark.category_id)).filter(
            Bookmark.category_id == Category._id,
            Bookmark.user_id == user._id).group_by(Category._id).paginate(
                page=request.args.get('page', 1), per_page=5)
    return render_template('list_categories.html', categories=categories)


@app.route('/users/<username>/categories/<name>')
def get_user_bookmarks_by_category(username, name):
    """Return current user's bookmarks according to category id passed."""
    try:
        user = db.query(User).filter_by(username=username).one()
        category = db.query(Category).filter_by(name=name).one()
    except NoResultFound:
        abort(404)
    bookmarks_users = db.query(Bookmark, User).filter(
        Bookmark.user_id == user._id).filter_by(category_id=category._id).join(
            User).paginate(page=request.args.get('page', 1), per_page=5)
    if not bookmarks_users:
        abort(404)
    if current_user.is_authenticated():
        votes = db.query(Vote).filter_by(
            user_id=current_user._id).all()
        for bookmark, _ in bookmarks_users:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    return render_template('list_bookmarks.html', category_name=name,
                           bookmarks=bookmarks_users)


@app.route('/users/<username>/bookmarks/<title>')
def get_user_bookmark_by_title(username, title):
    """Return user's bookmark according to title passed."""
    try:
        user = db.query(User).filter_by(username=username).one()
    except NoResultFound:
        abort(404)
    bookmark_user = db.query(Bookmark, User).filter(
        Bookmark.user_id == user._id).filter(Bookmark.title == title).join(
            User).paginate(page=1, per_page=1)
    category_name = ''
    if bookmark_user.showing:
        category_name = db.query(Category).get(
            bookmark_user.items[0][0].category_id).name
    return render_template('list_bookmarks.html', category_name=category_name,
                           bookmarks=bookmark_user)


@app.route('/users/<username>/bookmarks/')
def get_all_user_bookmarks(username):
    """Return all user's bookmarks."""
    try:
        user = db.query(User).filter_by(username=username).one()
    except NoResultFound:
        abort(404)
    bookmarks_user = db.query(Bookmark, User).filter(
        Bookmark.user_id == user._id).join(User).paginate(
            page=request.args.get('page', 1), per_page=5)
    if current_user.is_authenticated():
        votes = db.query(Vote).filter_by(
            user_id=current_user._id).all()
        for bookmark, _ in bookmarks_user:
            for vote in votes:
                if vote.bookmark_id == bookmark._id:
                    bookmark.vote = vote.direction
    return render_template('list_bookmarks.html', category_name='all',
                           bookmarks=bookmarks_user)


@app.route('/users/<username>/bookmarks/<title>/update',
           methods=['GET', 'POST'])
@login_required
def update_bookmark(username, title):
    """Update existing bookmark."""
    if username != current_user.username:
        raise Forbidden
    try:
        bookmark = db.query(Bookmark).filter(Bookmark.title == title).one()
    except NoResultFound:
        abort(404)
    if bookmark.user_id != current_user._id:
        raise Forbidden

    category = db.query(Category).get(bookmark.category_id)
    form = AddBookmarkForm()
    if form.validate_on_submit():
        # Check first if url changed and exists in other user's bookmarks
        if form.url.data != bookmark.url and db.query(Bookmark).filter(
            Bookmark.user_id != current_user._id).filter_by(
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


@app.route('/users/<username>/bookmarks/add', methods=['GET', 'POST'])
@login_required
def add_bookmark(username):
    """Add new bookmark to database."""
    if username != current_user.username:
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
                                category_id=category._id,
                                user_id=current_user._id)
            db.add(bookmark)
            db.commit()
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
                    db.add(category)
                    db.flush()
                    db.refresh(category)
                    if isinstance(value, list):
                        for link in value:
                            bookmark = Bookmark(title=urlparse(link).netloc,
                                                url=link,
                                                category_id=category._id,
                                                user_id=current_user._id)
                            db.add(bookmark)
                    elif isinstance(value, dict):
                        for title, link in value.items():
                            bookmark = Bookmark(title=title, url=link,
                                                category_id=category._id,
                                                user_id=current_user._id)
                            db.add(bookmark)
                db.commit()
            except Exception as e:
                db.rollback()
                with open('my_error_log.txt') as fob:
                    fob.write(str(e))
    return render_template('import_bookmarks.html')


@app.route('/bookmarks/<title>/vote', methods=['POST'])
@login_required
def vote_bookmark(title):
    """Vote up/down bookmark."""
    vote_direction = request.json.get('vote')
    if vote_direction not in range(-1, 2):
        raise BadRequest
    values = {-1: False, 0: None, 1: True}
    change = vote_direction
    try:
        bookmark = db.query(Bookmark).filter_by(title=title).one()
        vote = db.query(Vote).filter_by(user_id=current_user._id,
                                                bookmark_id=bookmark._id).one()
        if vote.direction is not None and vote_direction:
            vote.direction = values[vote_direction]
            change = 2 * vote_direction
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
        # Theres no vote record for this bookmark so create one.
        vote = Vote(direction=values[vote_direction], user_id=current_user._id,
                    bookmark_id=bookmark._id)
    try:
        bookmark = db.query(Bookmark).filter(
            Bookmark.user_id != current_user._id,
            Bookmark._id == bookmark._id).one()
    except NoResultFound:
        abort(404)
    bookmark.rating += change
    db.session.add_all([vote, bookmark])
    db.session.commit()
    return str(bookmark.rating)
