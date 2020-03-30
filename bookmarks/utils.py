"""Helper utilities."""

from flask import current_app

from .tasks import send_email_task


def send_email(subject, recipient, text):
    """Send email if configuration was set during app initiation."""
    api_key = current_app.config.get('SENDGRID_API_KEY')
    if not api_key:
        return False
    payload = {'subject': subject, 'text': text, 'recipients': [recipient],
               'from_email': current_app.config['MAIL_DEFAULT_SENDER']}
    send_email_task.delay(api_key, payload)
    return True
