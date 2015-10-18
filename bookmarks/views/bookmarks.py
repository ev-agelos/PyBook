"""Views for bookmark endpoints."""

from flask import render_template, abort, request, g
from flask.ext.login import login_required
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from werkzeug.exceptions import BadRequest

from bookmarks import app, db
from bookmarks.models import Bookmark, Category, Vote, User


@app.route('/')
def home():
    """Landing page with latest added bookmarks."""
    if g.user.is_authenticated():
        latest_bookmarks = db.query(Bookmark, User, Vote).join(User).outerjoin(
            Vote, Vote.bookmark_id == Bookmark._id).order_by(
            Bookmark.created_on.desc())
    else:
        latest_bookmarks = db.query(Bookmark, User).join(User).order_by(
            Bookmark.created_on.desc())
    paginator = latest_bookmarks.paginate(page=request.args.get('page', 1),
                                          per_page=5)
    return render_template('list_bookmarks.html', bookmarks=paginator,
                           category_name='all')


@app.route('/categories')
def get_categories():
    """Return paginator with all categories."""
    categories = db.query(
        Category.name, func.count(Bookmark.category_id)).filter(
            Bookmark.category_id == Category._id).group_by(Category._id)

    paginator = categories.paginate(page=request.args.get('page', 1),
                                    per_page=5)
    return render_template('list_categories.html', categories=paginator,
                           category_name='all')


@app.route('/bookmarks/')
def get_bookmarks():
    """
    Return paginator with all bookmarks.

    Join the users that submitted the bookmarks.
    If user is logged in, join possible votes he submitted. 
    """
    if g.user.is_authenticated():
        bookmarks = db.query(Bookmark, User, Vote).join(User).outerjoin(
            Vote, Vote.bookmark_id == Bookmark._id)
    else:
        bookmarks = db.query(Bookmark, User).join(User)
    paginator = bookmarks.paginate(page=request.args.get('page', 1),
                                   per_page=5)
    return render_template('list_bookmarks.html', bookmarks=paginator,
                           category_name='all')


@app.route('/categories/<name>')
def get_bookmarks_by_category(name):
    """
    Return paginator with bookmarks according to category name.

    Join the users that submitted the bookmarks.
    If user is logged in, join possible votes he submitted.
    """
    try:
        category = db.query(Category).filter_by(name=name).one()
    except NoResultFound:
        abort(404)
    if g.user.is_authenticated():
        bookmarks = db.query(Bookmark, User, Vote).filter(
            Bookmark.category_id == category._id).join(User).outerjoin(
                Vote, Vote.bookmark_id == Bookmark._id)
    else:
        bookmarks = db.query(Bookmark, User).filter(
            Bookmark.category_id == category._id).join(User)

    paginator = bookmarks.paginate(page=request.args.get('page', 1),
                                   per_page=5)
    return render_template('list_bookmarks.html', bookmarks=paginator,
                           category_name=name)


@app.route('/users/<username>/categories')
def get_categories_by_user(username):
    """Return paginator with all user's categories."""
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
    """Return paginator with user's bookmarks according to category <name>."""
    try:
        user = db.query(User).filter_by(username=username).one()
        category = db.query(Category).filter_by(name=name).one()
    except NoResultFound:
        abort(404)
    if g.user.is_authenticated():
        bookmarks = db.query(Bookmark, User, Vote).filter(
            Bookmark.user_id == user._id).filter_by(
                category_id=category._id).join(User).outerjoin(
                    Vote, Vote.bookmark_id == Bookmark._id)
    else:
        bookmarks = db.query(Bookmark, User).filter(
            Bookmark.user_id == user._id).filter_by(
                category_id=category._id).join(User)

    paginator = bookmarks.paginate(page=request.args.get('page', 1),
                                   per_page=5)
    return render_template('list_bookmarks.html', bookmarks=paginator,
                           category_name=name)


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
    if g.user.is_authenticated():
       bookmarks = db.query(Bookmark, User, Vote).join(User).filter(
        Bookmark.user_id == user._id).outerjoin(
            Vote, Vote.bookmark_id == Bookmark._id)
    else:
        bookmarks = db.query(Bookmark, User).join(User).filter(
            Bookmark.user_id == user._id)
    paginator = bookmarks.paginate(page=request.args.get('page', 1),
                                   per_page=5)
    return render_template('list_bookmarks.html', category_name='all',
                           bookmarks=paginator)


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
        vote = db.query(Vote).filter_by(user_id=g.user._id,
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
        vote = Vote(direction=values[vote_direction], user_id=g.user._id,
                    bookmark_id=bookmark._id)
    try:
        bookmark = db.query(Bookmark).filter(
            Bookmark.user_id != g.user._id, Bookmark._id == bookmark._id).one()
    except NoResultFound:
        abort(404)
    bookmark.rating += change
    db.session.add_all([vote, bookmark])
    db.session.commit()
    return str(bookmark.rating)
