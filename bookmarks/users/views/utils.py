"""Helper utilities."""


from flask import current_app
import requests


def send_email(subject, receiver, text):
    """Send email if configuration was set during app initiation."""
    mailgun_keys = ('MAILGUN_SENDER', 'MAILGUN_DOMAIN', 'MAILGUN_KEY')
    if not any(current_app.config.get(key) for key in mailgun_keys):
        return False

    payload = {'subject': subject, 'text': text, 'to': [receiver],
               'from': current_app.config['MAILGUN_SENDER']}
    response = requests.post(current_app.config['MAILGUN_DOMAIN'],
                             auth=('api', current_app.config['MAILGUN_KEY']),
                             data=payload)
    return response.status_code == 200
