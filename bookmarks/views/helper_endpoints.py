"""Helper endpoints that should requested internally."""


import re
from urllib.parse import urlparse

from flask import request, abort, Blueprint
from flask_login import login_required
from bs4 import BeautifulSoup
import requests


helper_endpoints = Blueprint('helper_endpoints', __name__)


@helper_endpoints.route('/suggest-title')
@login_required
def suggest_title():
    """Return the title of a given url."""
    url = request.args.get('url')
    if not url:
        abort(404)
    try:
        response = requests.get(url)
    except OSError:
        return urlparse(url).path.split('/')[-2].replace('-', ' ')
    if response.status_code != 200:
        return ''
    soup = BeautifulSoup(response.content, 'html.parser')
    if not soup.title:
        return ''
    title = soup.title.text
    # get rid of extraneous whitespace in the title
    title = re.sub(r'\s+', ' ', title, flags=re.UNICODE)
    return title
