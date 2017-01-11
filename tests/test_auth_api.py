from flask import g
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
