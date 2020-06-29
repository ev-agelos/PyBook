import re
from urllib.parse import urlparse

from flask_smorest import Blueprint
from flask_login import login_required
from bs4 import BeautifulSoup
import requests

from bookmarks import csrf

from .schemas import SuggestTitleArgsSchema, SuggestTitleResponseSchema


helper_api = Blueprint('helper_api', 'Helpers', url_prefix='/api/v1/',
                       description='Helper endpoints')


@helper_api.route('/suggest-title', methods=['POST'])
@helper_api.arguments(SuggestTitleArgsSchema)
@helper_api.response(SuggestTitleResponseSchema())
@csrf.exempt
@login_required
def suggest_title(args):
    """Fetch and return the title of a page."""
    try:
        response = requests.get(args['url'])
    except OSError:
        return urlparse(args['url']).path.split('/')[-2].replace('-', ' ')
    if not response.ok:
        return ''
    soup = BeautifulSoup(response.content, 'html.parser')
    if not soup.title:
        return ''
    title = soup.title.text
    # get rid of extraneous whitespace in the title
    title = re.sub(r'\s+', ' ', title, flags=re.UNICODE)
    return {'title': title}
