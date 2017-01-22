"""Helper functions."""

from threading import Thread
from urllib.parse import urljoin

from flask import current_app
import requests
from cloudinary import config, uploader
from bs4 import BeautifulSoup

from bookmarks import db
from bookmarks.models import Bookmark


def _scrape_img_url(html):
    """Search and return the image url from html code or return None."""
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find('meta', {'property': 'og:image'})
    return img_url.get('content') if img_url else None


def _fetch_img_and_upload(app, url, bookmark_id):
    """Fetch image url and upload it to cloudinary service."""
    config(cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
           api_key=app.config['CLOUDINARY_API_KEY'],
           api_secret=app.config['CLOUDINARY_SECRET_KEY'])
    response = uploader.upload(url)

    with app.app_context():  # update bookmark's image url
        bookmark = Bookmark.query.get(bookmark_id)
        bookmark.image = response['secure_url']
        db.session.add(bookmark)
        db.session.commit()


def get_url_thumbnail(url, bookmark_id):
    """Fetch and save url's related image if does not exist already locally."""
    response = requests.get(url)
    if response.status_code != 200:
        return None

    img_url = _scrape_img_url(response.content)
    if not img_url:  # otherwise fetch the favicon from the website
        img_url = urljoin(response.url, 'favicon.ico')
    app = current_app._get_current_object()
    thr = Thread(target=_fetch_img_and_upload, args=[app, img_url,
                                                     bookmark_id])
    thr.start()
