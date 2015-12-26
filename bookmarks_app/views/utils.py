"""Helper functions."""

from os.path import basename, isfile
from functools import wraps

from flask import request, render_template
from sqlalchemy_wrapper import Paginator
import requests
from bs4 import BeautifulSoup

from bookmarks_app import app, db


def paginate(serialized_query):
    """Return a query result paginated."""
    return Paginator(serialized_query, page=request.args.get('page', 1),
                     per_page=5)


def get_url_thumbnail(url):
    """Save url's image, if does not exist already locally."""
    # TODO optimization: get chunks of data until find the og:image
    # same to the script for suggesting the title.
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_has_link =  soup.find('meta', {'property': 'og:image'})
        img_link = None
        if img_has_link:
            img_link = img_has_link.get('content')
        if img_link is not None:
            img_name = basename(img_link)
            destination = app.static_folder + '/img/' + img_name
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


def render_it(template, check_thumbnails=False):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            result, category = func(*args, **kwargs) 
            if check_thumbnails:
                for models in result:
                    destination = app.static_folder + '/img/' + models[0]['thumbnail']
                    if not isfile(destination):
                        models[0]['thumbnail'] = 'default.png'
            return render_template(template, paginator=paginate(result),
                                   category_name=category)
        return wrapped
    return decorator


def serialize_models(query):
    """Serialize the models that are inside the query result."""
    bookmarks = []
    for result in query:
        row = []
        for model in result:
            if isinstance(model, db.Model):
                row.append(model.serialize().data)
        if row:
            bookmarks.append(tuple(row))
    return bookmarks
