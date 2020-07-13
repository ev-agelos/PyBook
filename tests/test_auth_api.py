"""Test cases for login/logout/register/account activation."""

from base64 import b64encode

import pytest
from flask_login import current_user

from bookmarks.users.models import User


@pytest.mark.parametrize('email,password', [
    ('mail#mail.com', 123),
    ('mail@.com', 123),
    ('@mail.com', 123),
    ('mail@mail.com', 123)
])
def test_invalid_login_form(api, email, password):
    auth = 'Basic ' + b64encode(f'{email}:{password}'.encode('ascii')).decode('ascii')
    rrr = api.post('/auth/request-token', headers=dict(Authorization=auth))
    assert rrr.status_code == 401


def test_login(app, user, api):
    auth = 'Basic ' + b64encode(f'{user.email}:123123'.encode('ascii')).decode('ascii')
    with app.test_client() as client:
        assert not current_user
        client.post(f'{api.path}/auth/request-token', headers=dict(Authorization=auth))
        assert current_user == user
    assert not current_user


def test_login_inactive_user(api, user, session):
    auth = 'Basic ' + b64encode(f'{user.email}:123123'.encode('ascii')).decode('ascii')
    user.active = False
    session.add(user)
    session.commit()
    r = api.post('/auth/request-token', headers=dict(Authorization=auth))
    assert r.status_code == 403 and 'Email address is not verified' in r.get_json()['message']


def test_login_with_wrong_password(api, user):
    auth = 'Basic ' + b64encode(f'{user.email}:wrongpass'.encode('ascii')).decode('ascii')
    r = api.post('/auth/request-token', headers=dict(Authorization=auth))
    assert r.status_code == 401


def test_api_logs_out_user(app, user, api):
    auth = 'Basic ' + b64encode(f'{user.email}:123123'.encode('ascii')).decode('ascii')
    with app.test_client() as client:
        client.post(f'{api.path}/auth/request-token', headers=dict(Authorization=auth))
        assert current_user.is_authenticated is True
        r = client.get(f'{api.path}/auth/logout', headers=dict(Authorization=auth))
        assert r.status_code == 204
        assert current_user.is_authenticated is False


@pytest.mark.parametrize('bad_data,msg', [
    ({'password': '123456789'}, 'Passwords must match'),
    ({'password': '1', 'confirmPassword': '1'}, ('Length must be between 8 and 25')),
    ({'email': '@mail.com'}, 'Not a valid email address'),
    ({'email': 'test_usermail.com'}, 'Not a valid email address'),
    ({'email': 'test_user@.com'}, 'Not a valid email address'),
    ({'email': 'test_user@mailcom'}, 'Not a valid email address'),
    ({'email': 'test_user@mail.'}, 'Not a valid email address'),
    ({'username': ''}, 'Length must be between 3 and 25')
])
def test_invalid_register_form(app, bad_data, msg, api):
    payload = {'username': 'test_user', 'email': 'test_user@mail.com',
               'password': '12345678', 'confirmPassword': '12345678',
               'recaptcha': 'foobar'}
    payload.update(bad_data)
    # use app instead of api to bypass token injection
    with app.test_client() as client:
        r = client.post(f'{api.path}/auth/register', json=payload)
        assert msg in str(r.get_json()['errors'])


def test_registering_user_with_others_user_email_and_username(app, user, api):
    payload = {'username': user.username, 'email': user.email,
               'password': '12312312', 'confirmPassword': '12312312',
               'recaptcha': 'foobar'}
    with app.test_client() as c:
        r = c.post(f'{api.path}/auth/register', json=payload)
        assert 'Username and email are already taken' in r.get_json()['message']


def test_registering_user_with_others_user_username(app, user, api):
    payload = {'username': user.username, 'email': 'random@mail.com',
               'password': '12312312', 'confirmPassword': '12312312',
               'recaptcha': 'foobar'}
    with app.test_client() as c:
        r = c.post(f'{api.path}/auth/register', json=payload)
        assert 'Username is already taken' in r.get_json()['message']


def test_registering_user_with_others_user_email(app, user, api):
    payload = {'username': 'random_username', 'email': user.email,
               'password': '12312312', 'confirmPassword': '12312312',
               'recaptcha': 'foobar'}
    with app.test_client() as c:
        r = c.post(f'{api.path}/auth/register', json=payload)
        assert 'Email is already taken' in r.get_json()['message']


def test_registering_a_new_user(app, session, api):
    payload = {'username': 'new_username', 'email': 'new@mail.com',
               'password': '12312312', 'confirmPassword': '12312312',
               'recaptcha': 'foobar'}
    with app.test_client() as c:
        r = c.post(f'{api.path}/auth/register', json=payload)
        assert 'A verification email has been sent' in r.get_json()['message']
    assert User.query.filter_by(username=payload['username'], email=payload['email'])


def test_activating_new_user(app, user, session, api):
    user.active = False
    session.add(user)
    session.commit()
    with app.test_client() as c:
        r = c.get(f'{api.path}/auth/confirm?token={user.auth_token}')
        assert user.active is True
        assert 'Your account has been activated' in r.get_json()['message']


def test_activating_already_activated_user(app, user, api):
    with app.test_client() as c:
        r = c.get(f'{api.path}/auth/confirm?token={user.auth_token}')
        assert 'account is already activated' in r.get_json()['message']


def test_activating_with_invalid_token(app, api):
    with app.test_client() as c:
        r = c.get(f'{api.path}/auth/confirm?token=aaaaaaaaaaaa')
        assert 'Confirmation link is invalid or has expired' in r.get_json()['message']


def test_activating_with_expired_token(app, user, monkeypatch, session, api):
    monkeypatch.setattr('bookmarks.users.models.User.verify_auth_token',
                        lambda *a, **kw: {})
    with app.test_client() as c:
        r = c.get(f'{api.path}/auth/confirm?token={user.auth_token}')
        assert 'Confirmation link is invalid or has expired' in r.get_json()['message']
