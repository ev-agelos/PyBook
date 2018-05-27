"""Helper utilities."""

from threading import Thread

from flask import current_app
from sparkpost import SparkPost


def _send_async_email(api_key, payload):
    """Helper function to be used by a Thread(to send the email)."""
    sp = SparkPost(api_key)
    sp.transmissions.send(**payload)


def send_email(subject, recipient, text):
    """Send email if configuration was set during app initiation."""
    api_key = current_app.config.get('SPARKPOST_API_KEY')
    if not api_key:
        return False
    payload = {'subject': subject, 'text': text, 'recipients': [recipient],
               'from_email': current_app.config['MAIL_DEFAULT_SENDER']}
    Thread(target=_send_async_email, args=[api_key, payload]).start()
    return True
