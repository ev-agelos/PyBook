"""Views for bookmark endpoints."""


from os.path import isfile

from flask import request, flash, render_template, current_app, g, Blueprint
from flask_login import login_required
from werkzeug.exceptions import Forbidden

from bookmarks import db, csrf

from ..models import Bookmark, Category
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
        return _post(form)
    category_list = db.session.query(Category).all()
    return render_template('bookmarks/add.html', form=form,
                           category_list=category_list)


@bookmarks.route('/bookmarks/<int:id>/update', methods=['GET', 'PUT'])
@login_required
def update(id):
    """Return form for updating a bookmark."""
    if request.method == 'PUT':
        form = UpdateBookmarkForm()
        return _put(id, form)

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
    return _delete(id)


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
    return _save(id)


@bookmarks.route('/bookmarks/<int:id>/unsave', methods=['DELETE'])
@csrf.exempt
@login_required
def unsave(id):
    """Un-save bookmark to user's listings."""
    return _unsave(id)


@bookmarks.route('/bookmarks/<int:id>/vote', methods=['POST', 'PUT', 'DELETE'])
@login_required
def vote(id):
    """Vote a bookmark."""
    methods = {'POST': _post_vote, 'PUT': _put_vote}
    return methods.get(request.method, _delete_vote)(id)
