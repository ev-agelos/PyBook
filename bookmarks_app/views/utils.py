"""Helper functions."""

from os.path import basename, isfile

from flask import request
import requests
from bs4 import BeautifulSoup

from bookmarks_app import app


def paginate(query):
    """Return a query result paginated."""
    return query.paginate(page=request.args.get('page', 1), per_page=5)


def get_url_thumbnail(url):
    """Save url's image, if does not exist already locally."""
    # TODO optimization: get chunks of data until find the og:image
    # same to the script for suggesting the title.
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_link =  soup.find('meta', {'property': 'og:image'})['content']
        img_name = basename(img_link)
        destination = app.static_folder + '/img/' + img_name
        if not isfile(destination):
            img_response = requests.get(url, stream=True)
            if img_response.status_code == 200:
                with open(destination, 'wb') as fob:
                    for chunk in img_response:
                        fob.write(chunk)
            else:
                # TODO if not accessible i should re-try to download
                return None
        return img_name
    return None
