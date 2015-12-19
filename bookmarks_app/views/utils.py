"""Helper functions."""

from os.path import basename

from flask import request
import requests
from bs4 import BeautifulSoup

from bookmarks_app import app


def paginate(query):
    """Return a query result paginated."""
    return query.paginate(page=request.args.get('page', 1), per_page=5)


def get_url_thumbnail(url):
    """Save url's image, if found."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_found = soup.find('meta', {'property': 'og:image'})
        if img_found:
            img_response = requests.get(img_found['content'], stream=True)
            if img_response.status_code == 200:
                img_name = basename(img_found['content'])
                destination = app.static_folder + '/img/' + img_name
                with open(destination, 'wb') as fob:
                    for chunk in img_response:
                        fob.write(chunk)
