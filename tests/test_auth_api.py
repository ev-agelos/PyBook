import base64
import time

from flask import g

from bookmarks.api.auth import verify_password, verify_token


def test_basic_auth_sets_user_in_g(app, user):
    with app.app_context():
        assert not hasattr(g, 'user')
        assert verify_password(user.email, '123123')
        assert g.user == user


def test_basic_auth_with_bad_email_doesnt_set_user_to_g(app):
    with app.app_context():
        assert not verify_password('bad@email.com', '123123')
        assert g.user is None


def test_basic_auth_with_wrong_password_that_sets_user_to_g(app, user):
    with app.app_context():
        assert not verify_password(user.email, '111111')
        assert g.user == user


def test_token_auth_with_wrong_token_doesnt_set_user_to_g(app):
    with app.app_context():
        verify_token('wrong_token')
        assert not hasattr(g, 'user')


def test_requesting_new_token(user, session, api):
    credentials = bytes("{}:{}".format(user.email, '123123'), 'ascii')
    auth = base64.b64encode(credentials).decode('ascii')
    time.sleep(1)  # for itsdangerous to create new token
    resp = api.post('/auth/request-token',
                    headers={'Authorization': 'Basic ' + auth})
    assert resp.status_code == 200 and resp.get_json()['token'] and \
        resp.get_json()['token'] != user.auth_token
