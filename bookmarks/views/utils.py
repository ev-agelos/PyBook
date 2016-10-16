"""Helper functions."""

from os.path import basename, isfile
from functools import wraps

from flask import request, render_template, current_app
from sqlalchemy_wrapper import Paginator
import requests
from bs4 import BeautifulSoup


def paginate(query):
    """Return a query result paginated."""
    return Paginator(query, page=request.args.get('page', 1), per_page=5)


def get_url_thumbnail(url):
    """Save url's image, if does not exist already locally."""
    # TODO optimization: get chunks of data until find the og:image
    # same to the script for suggesting the title.
    try:
        response = requests.get(url)
    except OSError: # Host might now allow extenrnal requests
        return None
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_has_link =  soup.find('meta', {'property': 'og:image'})
        img_link = None
        if img_has_link:
            img_link = img_has_link.get('content')
        if img_link is not None:
            img_name = basename(img_link)
            destination = current_app.static_folder + '/img/' + img_name
            if not isfile(destination):
                img_response = requests.get(img_link, stream=True)
                if img_response.status_code == 200:
                    with open(destination, 'wb') as fob:
                        for chunk in img_response:
                            fob.write(chunk)
                else:
                    # TODO if not accessible i should re-try to download
                    return None
            return img_name
    return None


def custom_render(template, check_thumbnails=False):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            query, category = func(*args, **kwargs)
            if check_thumbnails:
                for bookmark in query:
                    if bookmark.image is not None:
                        file_path = current_app.static_folder + '/img/' + \
                            bookmark.image
                        if not isfile(file_path):  # Maybe image was deleted
                            bookmark.image = None
            return render_template(template, paginator=paginate(query),
                                   category_name=category)
        return wrapped
    return decorator
