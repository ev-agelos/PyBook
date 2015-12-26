"""Helper endpoints that should requested internally."""


import re

from flask import request, abort
from flask_login import login_required
from bs4 import BeautifulSoup
import requests

from bookmarks_app import app


@app.route('/suggest-title')
@login_required
def suggest_title():
    """Return the title of a given url."""
    url = request.args.get('url')
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.text
        # get rid of extraneous whitespace in the title
        title = re.sub(r'\s+', ' ', title, flags=re.UNICODE)
        return title
    else:
        abort(404)
