import sendgrid
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent

from bookmarks import celery


@celery.task
def send_email_task(api_key, payload):
    """Send email."""
    sg = sendgrid.SendGridAPIClient(api_key)
    mail = Mail(
        From(payload['from_email']),
        To(*payload['recipients']),
        Subject(payload['subject']),
        plain_text_content=PlainTextContent(payload['text'])
    )
    sg.send(mail)
