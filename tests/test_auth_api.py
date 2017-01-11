import base64

from flask import g, json
from bookmarks.api.auth import verify_password, verify_token, request_token


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


def test_requesting_new_token(app, user, session):
    credentials = bytes("{}:{}".format(user.email, '123123'), 'ascii')
    auth = base64.b64encode(credentials).decode('ascii')
    import time;time.sleep(1)  # for itsdangerous to create new token
    resp = app.test_client().post('/api/auth/request-token',
                                  headers={'Authorization': 'Basic ' + auth})
    assert resp.status_code == 200
    assert json.loads(resp.data)['token']
    assert json.loads(resp.data)['token'] != user.auth_token
