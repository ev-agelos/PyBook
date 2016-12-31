"""Helper utilities."""

from threading import Thread

from flask import current_app
import requests


def _send_async_email(app, payload):
    """Make the request to send the email asynchronously."""
    requests.post(app.config['MAIL_DOMAIN'],
                  auth=('api', app.config['MAIL_KEY']), data=payload)


def send_email(subject, receiver, text):
    """Send email if configuration was set during app initiation."""
    mailgun_keys = ('MAIL_DEFAULT_SENDER', 'MAIL_DOMAIN', 'MAIL_KEY')
    if not any(current_app.config.get(key) for key in mailgun_keys):
        return False

    payload = {'subject': subject, 'text': text, 'to': [receiver],
               'from': current_app.config['MAIL_DEFAULT_SENDER']}
    app = current_app._get_current_object()
    thr = Thread(target=_send_async_email, args=[app, payload])
    thr.start()
    return True
