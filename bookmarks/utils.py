"""Helper utilities."""

from threading import Thread

from flask import current_app
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent


def _send_async_email(api_key, payload):
    """Helper function to be used by a Thread(to send the email)."""
    sg = sendgrid.SendGridAPIClient(api_key)
    mail = Mail(
        From(payload['from_email']),
        To(*payload['recipients']),
        Subject(payload['subject']),
        plain_text_content=PlainTextContent(payload['text'])
    )
    sg.send(mail)


def send_email(subject, recipient, text):
    """Send email if configuration was set during app initiation."""
    api_key = current_app.config.get('SENDGRID_API_KEY')
    if not api_key:
        return False
    payload = {'subject': subject, 'text': text, 'recipients': [recipient],
               'from_email': current_app.config['MAIL_DEFAULT_SENDER']}
    Thread(target=_send_async_email, args=[api_key, payload]).start()
    return True
