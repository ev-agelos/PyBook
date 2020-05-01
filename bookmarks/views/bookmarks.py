"""Views for bookmark endpoints."""


from flask import (request, flash, render_template, g, Blueprint, jsonify,
                   url_for)
from flask_login import login_required
from werkzeug.exceptions import Forbidden
from webargs.flaskparser import use_args

from bookmarks import db
from bookmarks.api.schemas import (
    BookmarksQueryArgsSchema
)
from ..models import Bookmark, Tag, Favourite, Vote, VoteSchema
from ..forms import AddBookmarkForm, UpdateBookmarkForm
from ..logic import (_get, _post, _put, _delete, _save, _unsave, _post_vote,
                     _put_vote, _delete_vote)

bookmarks = Blueprint('bookmarks', __name__)


@bookmarks.route('/bookmarks/')
@use_args(BookmarksQueryArgsSchema())
def get(args):
    """Return all bookmarks with the tag name."""
    query = _get(args)
    pag = query.paginate(page=request.args.get('page', 1, type=int),
                         per_page=5)
    if g.user and g.user.is_authenticated:
        user_votes = g.user.votes.all()
        for bookmark in pag.items:
            for vote in user_votes:
                if bookmark.id == vote.bookmark_id:
                    bookmark.vote = vote.direction
                    break
    return render_template('bookmarks/list_bookmarks.html',
                           form=AddBookmarkForm(),
                           paginator=pag, tag_name='all')


@bookmarks.route('/bookmarks/add', methods=['POST'])
@login_required
def add():
    """Add new bookmark."""
    form = AddBookmarkForm()
    if not form.validate():
        return jsonify(message='invalid data', status=400), 400
    bookmark = Bookmark.query.filter_by(url=form.url.data).scalar()
    if bookmark is not None:
        return jsonify(message='bookmark already exists', status=409), 409
    bookmark_id = _post(form.data)
    response = jsonify({})
    response.status_code = 201
    response.headers['Location'] = url_for(
        'bookmarks_api.BookmarkAPI', id=bookmark_id, _external=True)
    return response


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
        _put(id, form.data)
        return jsonify(message='Bookmark updated', status=200), 200

    bookmark = Bookmark.query.get_or_404(id)
    if bookmark.user != g.user:
        raise Forbidden
    tags = db.session.query(Tag).all()
    form = UpdateBookmarkForm(tags=[tag.name for tag in bookmark.tags],
                              title=bookmark.title, url=bookmark.url)
    return render_template('bookmarks/update.html', bookmark_id=id,
                           form=form, tag_list=tags)


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
    pag = Bookmark.query.filter_by(id=None).paginate(
        page=request.args.get('page', 1, type=int), per_page=5)
    return render_template('bookmarks/list_bookmarks.html', paginator=pag)


@bookmarks.route('/bookmarks/<int:id>/save', methods=['POST'])
@login_required
def save(id):
    """Save bookmark to user's listings."""
    if Favourite.query.filter_by(user_id=g.user.id,
                                 bookmark_id=id).scalar() is not None:
        return jsonify(message='bookmark already saved', status=409), 409
    _save(id)
    response = jsonify({})
    response.status_code = 201
    return response


@bookmarks.route('/bookmarks/<int:id>/unsave', methods=['DELETE'])
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
        _put_vote(vote_, direction, vote_arg)
        return VoteSchema().jsonify(vote_), 200
    else:
        if vote_ is None:
            return jsonify(message='no vote found for the given bookmark_id',
                           status=404), 404
        elif vote_.user_id != g.user.id:
            return jsonify(message='forbidden', status=403), 403
        _delete_vote(vote_)
        return jsonify({}), 204
