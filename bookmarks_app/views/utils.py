"""Helper functions."""

from os.path import basename

from flask import request
import requests
from bs4 import BeautifulSoup

from bookmarks_app import app


def paginate(query):
    """Return a query result paginated."""
    return query.paginate(page=request.args.get('page', 1), per_page=5)


def url_has_img(url):
    """Look if url has an image in the form of og:image in it's content."""
    # TODO optimization: get chunks of data until find the og:image
    # same to the script for suggesting the title.
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find('meta', {'property': 'og:image'})['content']
    return None
        

def get_url_thumbnail(url):
    """Save url's image."""
    img_response = requests.get(url, stream=True)
    if img_response.status_code == 200:
        img_name = basename(url)
        destination = app.static_folder + '/img/' + img_name
        with open(destination, 'wb') as fob:
            for chunk in img_response:
                fob.write(chunk)
        return img_name
    return None
