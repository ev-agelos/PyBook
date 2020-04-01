"""Helper functions."""

from threading import Thread
from urllib.parse import urljoin
import re

from flask import current_app
import requests
from cloudinary import config, uploader
from bs4 import BeautifulSoup

from bookmarks import db
from bookmarks.models import Bookmark


def _scrape_img_url(html, url):
    """Search and return the image url from html code or return None."""
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find('meta', {'property': 'og:image'})
    if img_url:
        return img_url.get('content')
    logo = soup.head.find('img', src=re.compile('logo'))
    if logo:
        return urljoin(url, logo['src'])
    favicon = soup.head.find('link', href=re.compile('favicon'))
    if favicon:
        return urljoin(url, favicon['href'])
    return None


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
    cloudinary_config = (
        'CLOUDINARY_SECRET_KEY',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_CLOUD_NAME'
    )
    if not all(current_app.config.get(k) for k in cloudinary_config):
        return None
    response = requests.get(url)
    if response.status_code != 200:
        return None

    img_url = _scrape_img_url(response.content, url)
    if img_url:
        app = current_app._get_current_object()
        Thread(target=_fetch_img_and_upload,
                args=[app, img_url, bookmark_id]).start()
