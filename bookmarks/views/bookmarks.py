"""Views for bookmark endpoints."""


from os.path import isfile

from flask import (request, flash, render_template, current_app, g, Blueprint,
                   jsonify, url_for)
from flask_login import login_required
from werkzeug.exceptions import Forbidden

from bookmarks import db, csrf

from ..models import Bookmark, Category, Favourite, Vote, VoteSchema
from ..forms import AddBookmarkForm, UpdateBookmarkForm
from ..logic import (_get, _post, _put, _delete, _save, _unsave, _post_vote,
                     _put_vote, _delete_vote)

bookmarks = Blueprint('bookmarks', __name__)


@bookmarks.route('/bookmarks/')
def get():
    """Return all bookmarks with the category name."""
    query = _get()
    for bookmark in query:
        if bookmark.image is not None:
            file_path = current_app.static_folder + '/img/' + \
                bookmark.image
            if not isfile(file_path):  # Maybe image was deleted
                bookmark.image = None

    pag = query.paginate(page=request.args.get('page', 1, type=int),
                         per_page=5)
    if g.user and g.user.is_authenticated:
        user_votes = g.user.votes.all()
        user_vote_bookmarks = [vote.bookmark_id for vote in user_votes]
        for bookmark in pag.items:
            for vote in user_votes:
                if bookmark.id == vote.bookmark_id:
                    bookmark.vote = vote.direction
                    break
    return render_template('bookmarks/list_bookmarks.html',
                           paginator=pag, category_name='all')


@bookmarks.route('/bookmarks/add', methods=['GET', 'POST'])
@login_required
def add():
    """Return form for adding new bookmark."""
    form = AddBookmarkForm()
    if request.method == 'POST':
        if not form.validate():
            return jsonify(message='invalid data', status=400), 400
        bookmark = Bookmark.query.filter_by(url=form.url.data).scalar()
        if bookmark is not None:
            return jsonify(message='bookmark already exists', status=409), 409
        bookmark_id = _post(form)
        response = jsonify({})
        response.status_code = 201
        response.headers['Location'] = url_for(
            'bookmarks_api.get', id=bookmark_id, _external=True)
        return response
    category_list = db.session.query(Category).all()
    return render_template('bookmarks/add.html', form=form,
                           category_list=category_list)


@bookmarks.route('/bookmarks/<int:id>/update', methods=['GET', 'PUT'])
@login_required
def update(id):
    """Return form for updating a bookmark."""
    if request.method == 'PUT':
        form = UpdateBookmarkForm()
        if not form.validate():
            return jsonify(message='invalid data', status=400), 400
        bookmark = Bookmark.query.get(id)
        if bookmark is None:
            return jsonify(message='Bookmark does not exist', status=404), 404
        if form.url.data and form.url.data != bookmark.url:
            existing_url = Bookmark.query.filter_by(url=form.url.data).scalar()
            if existing_url is not None:
                return jsonify(message='url already exists', status=409), 409
        _put(id, form)
        return jsonify(message='Bookmark updated', status=200), 200

    bookmark = Bookmark.query.get_or_404(id)
    if bookmark.user != g.user:
        raise Forbidden
    categories = db.session.query(Category).all()
    form = UpdateBookmarkForm(category=bookmark.category.name,
                              title=bookmark.title, url=bookmark.url)
    return render_template('bookmarks/update.html', bookmark_id=id,
                           form=form, category_list=categories)


@bookmarks.route('/bookmarks/<int:id>/delete', methods=['DELETE'])
@login_required
def delete(id):
    """Delete a bookmark."""
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='not found', status=404), 404
    if bookmark.user_id != g.user.id:
        return jsonify(message='forbidden', status=403), 403
    _delete(id)
    return jsonify({}), 204


@bookmarks.route('/bookmarks/search')
def search():
    """Search bookmarks."""
    flash('Sorry, search is not implemented yet :(', 'info')
    return ([], 'all')


@bookmarks.route('/bookmarks/<int:id>/save', methods=['POST'])
@csrf.exempt
@login_required
def save(id):
    """Save bookmark to user's listings."""
    # TODO research if such views need csrf protection
    if Favourite.query.filter_by(user_id=g.user.id,
                                 bookmark_id=id).scalar() is not None:
        return jsonify(message='bookmark already saved', status=409), 409
    _save(bookmark_id)
    response = jsonify({})
    response.status_code = 201
    return response


@bookmarks.route('/bookmarks/<int:id>/unsave', methods=['DELETE'])
@csrf.exempt
@login_required
def unsave(id):
    """Un-save bookmark to user's listings."""
    favourite = Favourite.query.filter_by(user_id=g.user.id,
                                          bookmark_id=id).scalar()
    if favourite is None:
        return jsonify(message='save not found', status=404), 404
    _unsave(favourite)
    return jsonify({}), 204


@bookmarks.route('/bookmarks/<int:id>/vote', methods=['POST', 'PUT', 'DELETE'])
@login_required
def vote(id):
    """Vote a bookmark."""
    if request.method in ('POST', 'PUT'):
        vote_arg = request.get_json().get('vote')
        direction = {1: True, -1: False}.get(vote_arg)
        if direction is None:
            return jsonify(message='invalid data', status=400), 400
    bookmark = Bookmark.query.get(id)
    if bookmark is None:
        return jsonify(message='bookmark not found', status=404), 404
    vote_ = Vote.query.filter_by(user_id=g.user.id, bookmark_id=id).scalar()

    if request.method == 'POST':
        if vote_ is not None:
            return jsonify(message='vote already exists', status=409), 409
        _post_vote(bookmark, direction, vote_arg)
        response = jsonify({})
        response.status_code = 201
        return response
    elif request.method == 'PUT':
        if vote_ is None:
            return jsonify(message='vote not found', status=404), 404
        elif direction == vote_.direction:
            return jsonify(message='bookmark is voted with {} already'
                           .format('+1' if vote == 1 else '-1'),
                           status=409), 409
        _put_vote(vote, direction, vote_arg)
        return VoteSchema().jsonify(vote_), 200
    else:
        if vote_ is None:
            return jsonify(message='no vote found for the given bookmark_id',
                           status=404), 404
        elif vote_.user_id != g.user.id:
            return jsonify(message='forbidden', status=403), 403
        _delete_vote(vote)
        return jsonify({}), 204
