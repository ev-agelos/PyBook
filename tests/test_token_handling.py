import time

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import pytest


def test_creating_token_includes_user_id(app, user):
    with app.app_context():
        token = user.generate_auth_token()
    serializer = Serializer(app.config['SECRET_KEY'])
    assert serializer.loads(token)['id'] == user.id


def test_valid_token_gets_confirmed(app, user):
    secret_key = app.config['SECRET_KEY']
    serializer = Serializer(secret_key)
    token = serializer.dumps({'id': user.id})
    with app.app_context():
        assert user.verify_auth_token(token) == user


def test_expired_token(app, user):
    secret_key = app.config['SECRET_KEY']
    serializer = Serializer(secret_key, expires_in=0)
    token = serializer.dumps({'id': user.id})
    time.sleep(1)
    with app.app_context():
        assert user.verify_auth_token(token) is None
