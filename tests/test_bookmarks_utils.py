import pytest

from bookmarks.utils import send_email


def test_sending_email_without_credentials(app):
    with app.app_context():
        assert not send_email('a', 'b', 'c')


def test_sending_email_with_credentials(app):
    with app.app_context():
        app.config.update(MAIL_DEFAULT_SENDER='a', SENDGRID_API_KEY='c')
        assert send_email('a', 'b', 'c')
