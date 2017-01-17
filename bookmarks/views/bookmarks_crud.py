"""CRUD endpoints for bookmarks."""

import json
from urllib.parse import urlparse

from flask import render_template, request, g, Blueprint
from flask_login import login_required
from werkzeug.utils import secure_filename

from bookmarks import db

from ..models import Tag, Bookmark


crud = Blueprint('crud', __name__)


@crud.route('/bookmarks/import', methods=['GET', 'POST'])
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
                for tag_name, value in json_data.items():
                    tag = Tag(name=tag_name.lower())
                    db.session.add(tag)
                    db.session.flush()
                    db.session.refresh(tag)
                    if isinstance(value, list):
                        for link in value:
                            bookmark = Bookmark(
                                title=urlparse(link).netloc, url=link,
                                tag_id=tag.id, user_id=g.user.id)
                            db.session.add(bookmark)
                    elif isinstance(value, dict):
                        for title, link in value.items():
                            bookmark = Bookmark(title=title, url=link,
                                                tag_id=tag.id,
                                                user_id=g.user.id)
                            db.session.add(bookmark)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                with open('my_error_log.txt') as fob:
                    fob.write(str(e))
    return render_template('bookmarks/import_bookmarks.html')
