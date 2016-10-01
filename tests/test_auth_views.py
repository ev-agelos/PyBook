"""Test cases for login/logout/register/account activation."""

import pytest
from flask_login import current_user

from bookmarks.auth.models import User


def test_login_get_request_returns_html(app):
    r = app.test_client().get('/login')
    assert b'<title>Login</title>' in r.data


@pytest.mark.parametrize('email,password', [
    ('mail#mail.com', 123),
    ('mail@.com', 123),
    ('@mail.com', 123),
    ('mail@mail.com', 123)
])
def test_invalid_login_form(app, email, password):
    r = app.test_client().post('/login', data=dict(email=email,
                                                   password=password))
    assert r.status_code == 200
    assert b'<title>Login</title>' in r.data


def test_login(app, user):
    with app.test_client() as c:
        assert not current_user
        r = c.post('/login', data=dict(email=user.email, password='123123'),
                   follow_redirects=True)
        assert current_user == user


def test_login_inactive_user(app, user, session):
    user.active = False
    session.add(user)
    session.commit()
    with app.test_client() as c:
        r = c.post('/login', data=dict(email=user.email, password='123123'),
                   follow_redirects=True)
        assert b'Email address is not verified' in r.data


def test_login_with_wrong_password(app, user):
    with app.test_client() as c:
        r = c.post('/login', data=dict(email=user.email, password='111111'),
                   follow_redirects=True)
        assert b'Wrong credentials' in r.data


def test_logout(app, user):
    with app.test_client() as c:
        c.post('/login', data=dict(email=user.email, password='123123'),
               follow_redirects=True)
        assert current_user.is_authenticated
        r = c.get('/logout', follow_redirects=True)
        assert not current_user.is_authenticated
        assert b'You have been logged out' in r.data


def test_getting_register_form(app):
    with app.test_client() as c:
        r = c.get('/register', follow_redirects=True)
        assert b'<title>Register</title>' in r.data


@pytest.mark.parametrize('bad_data,msg', [
    ({'password': '123'}, 'Passwords must match'),
    ({'password': '1', 'confirm_password': '1'}, ('Field must be between 6 and'
                                                  ' 25 characters long')),
    ({'email': '@mail.com'}, 'Invalid email address'),
    ({'email': 'test_usermail.com'}, 'Invalid email address'),
    ({'email': 'test_user@.com'}, 'Invalid email address'),
    ({'email': 'test_user@mailcom'}, 'Invalid email address'),
    ({'email': 'test_user@mail.'}, 'Invalid email address'),
    ({'username': ''}, 'This field is required')
])
def test_invalid_register_form(app, bad_data, msg):
    payload = {'username': 'test_user', 'email': 'test_user@mail.com',
               'password': '123456', 'confirm_password': '123456'}
    payload.update(bad_data)
    with app.test_client() as c:
        r = c.post('/register', data=payload, follow_redirects=True)
        assert msg.encode() in r.data


def test_registering_user_with_others_user_email_and_username(app, user):
    payload = {'username': user.username, 'email': user.email,
               'password': '123123', 'confirm_password': '123123'}
    with app.test_client() as c:
        r = c.post('/register', data=payload, follow_redirects=True)
        assert b'Username and email are already taken' in r.data


def test_registering_user_with_others_user_username(app, user):
    payload = {'username': user.username, 'email': 'random@mail.com',
               'password': '123123', 'confirm_password': '123123'}
    with app.test_client() as c:
        r = c.post('/register', data=payload, follow_redirects=True)
        assert b'Username is already taken' in r.data


def test_registering_user_with_others_user_email(app, user):
    payload = {'username': 'random_username', 'email': user.email,
               'password': '123123', 'confirm_password': '123123'}
    with app.test_client() as c:
        r = c.post('/register', data=payload, follow_redirects=True)
        assert b'Email is already taken' in r.data


def test_registering_a_new_user(app):
    payload = {'username': 'new_username', 'email': 'new@mail.com',
               'password': '123123', 'confirm_password': '123123'}
    with app.test_client() as c:
        r = c.post('/register', data=payload, follow_redirects=True)
        assert b'A verification email has been sent' in r.data
    assert User.query.filter_by(username=payload['username'],
                                email=payload['email'])


def test_activating_new_user(app, user, session):
    user.active = False
    session.add(user)
    session.commit()
    with app.test_client() as c:
        r = c.get('/users/activate/' + user.email_token, follow_redirects=True)
        assert user.is_active
        assert b'Your account has been activated' in r.data


def test_activating_already_activated_user(app, user):
    with app.test_client() as c:
        r = c.get('/users/activate/' + user.email_token, follow_redirects=True)
        assert b'account is already activated' in r.data


def test_activating_with_invalid_token(app):
    with app.test_client() as c:
        r = c.get('/users/activate/invalid', follow_redirects=True)
        assert b'Confirmation link is invalid or has expired' in r.data


def test_activating_with_expired_token(app, user, monkeypatch):
    monkeypatch.setattr('bookmarks.auth.token.confirm', lambda *a, **kw: False)
    with app.test_client() as c:
        r = c.get('/users/activate/' + user.email_token, follow_redirects=True)
        assert b'Confirmation link is invalid or has expired' in r.data
