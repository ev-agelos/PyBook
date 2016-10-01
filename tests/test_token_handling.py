import time

from itsdangerous import URLSafeTimedSerializer
import pytest

from bookmarks.auth import token as token_


def test_creating_token_includes_passed_email(app):
    email = 'test_user@mail.com'
    secret_key = app.config['SECRET_KEY']
    with app.app_context():
        token = token_.generate(email, secret_key)
    serializer = URLSafeTimedSerializer(secret_key)
    assert serializer.loads(token) == email


def test_valid_token_gets_confirmed(app):
    email = 'email@mail.com'
    secret_key = app.config['SECRET_KEY']
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps(email)
    with app.app_context():
        assert token_.confirm(token, secret_key) == email


def test_expired_token(app):
    email = 'email@mail.com'
    secret_key = app.config['SECRET_KEY']
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps(email)
    time.sleep(1)
    with app.app_context():
        assert not token_.confirm(token, secret_key, expiration=0)
