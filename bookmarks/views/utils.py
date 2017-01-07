"""Helper functions."""

from os.path import basename, isfile
from threading import Thread
from urllib.parse import quote_plus, urljoin

from flask import current_app
import requests
from bs4 import BeautifulSoup


def _find_img_url(html):
    """Search and return the image url from html code or None."""
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find('meta', {'property': 'og:image'})
    return img_url.get('content') if img_url else None


def _download_image(url, filepath):
    """Download image and save it to disk."""
    img_response = requests.get(url, stream=True)
    if img_response.status_code == 200:
        with open(filepath, 'wb') as fob:
            for chunk in img_response:
                fob.write(chunk)


def get_url_thumbnail(url):
    """Fetch and save url's related image if does not exist already locally."""
    try:
        response = requests.get(url)
    except OSError:  # Host might not allow external requests
        return None
    if response.status_code != 200:
        return None

    img_name = ''
    img_url = _find_img_url(response.content)
    if img_url:
        img_name = basename(img_url)
    else:  # try to download the favicon from the url
        img_name = quote_plus(response.url)
        img_url = urljoin(response.url, 'favicon.ico')

    filepath = current_app.static_folder + '/img/' + img_name
    if not isfile(filepath):  # download only if it doesn't exist
        thr = Thread(target=_download_image, args=[img_url, filepath])
        thr.start()
    return img_name
