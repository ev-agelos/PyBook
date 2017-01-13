from flask import json

from bookmarks.users.models import User, UserSchema, SubscriptionsSchema
from bookmarks.models import (Bookmark, Vote, Favourite, VoteSchema,
                              FavouriteSchema)


def test_getting_all_users(app, user):
    resp = app.test_client().get(
        '/api/users/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    with app.test_request_context():
        users_json = UserSchema(many=True).dump([user]).data
    assert json.loads(resp.data)['users'] == users_json


def test_getting_self_user(app, user):
    resp = app.test_client().get(
        '/api/users/1',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    with app.test_request_context():
        user_json = UserSchema().dump(user).data
    assert json.loads(resp.data) == user_json


def test_getting_different_user(app, user, session):
    user_9 = User(id=9)
    session.add(user_9)
    session.commit()
    resp = app.test_client().get(
        '/api/users/9',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    with app.test_request_context():
        user_json = UserSchema().dump(user_9).data
    assert json.loads(resp.data) == user_json


def test_getting_one_user_that_doesnt_exist(app, user):
    resp = app.test_client().get(
        '/api/users/999',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 404
    assert 'User not found' in json.loads(resp.data)['message']


def test_delete_self_user(app, user, session):
    resp = app.test_client().delete(
        '/api/users/1',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 204
    assert User.query.get(user.id) is None


def test_delete_different_user(app, user, session):
    resp = app.test_client().delete(
        '/api/users/999',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 403


def test_delete_user_deletes_his_favourites(app, user, session):
    favourite = Favourite(user_id=user.id, bookmark_id=999)
    session.add(favourite)
    session.commit()
    resp = app.test_client().delete(
        '/api/users/1',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert Favourite.query.filter_by(user_id=user.id).scalar() is None


def test_get_votes_from_different_user(app, user):
    resp = app.test_client().get(
        '/api/users/999/votes',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 403


def test_get_user_votes(app, user, session):
    b_1 = Bookmark(id=1)
    vote = Vote(user_id=user.id, bookmark_id=b_1.id, direction=False)
    session.add(vote)
    session.add(b_1)
    session.commit()
    resp = app.test_client().get(
        '/api/users/1/votes',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 200
    resp_votes = json.loads(resp.data)['votes']
    assert resp_votes == VoteSchema(many=True).dump([vote]).data


def test_get_favourites_from_different_user(app, user):
    resp = app.test_client().get(
        '/api/users/999/favourites',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 403


def test_get_user_favourites(app, user, session):
    b_1 = Bookmark(id=1)
    favourite = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(favourite)
    session.add(b_1)
    session.commit()
    resp = app.test_client().get(
        '/api/users/1/favourites',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 200
    resp_favourites = json.loads(resp.data)['favourites']
    assert resp_favourites == FavouriteSchema(many=True).dump([favourite]).data


def test_get_subscribers_from_user_that_doesnt_exist(app, user):
    resp = app.test_client().get(
        '/api/users/999/subscribers',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 404
    assert 'User not found' in json.loads(resp.data)['message']


def test_get_user_subscribers(app, user, session):
    user_2 = User() 
    session.add(user_2)
    session.commit()
    user_2.subscribe(user)
    resp = app.test_client().get(
        '/api/users/1/subscribers',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 200
    resp_subscribers = json.loads(resp.data)['subscribers']
    assert resp_subscribers == SubscriptionsSchema(many=True).dump([user_2]).data


def test_subscribing_to_yourself(app, user):
    resp = app.test_client().post(
        '/api/users/1/subscribe',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 400
    assert 'Cannot subscribe to yourself' in json.loads(resp.data)['message']


def test_subscribing_to_user_that_doesnt_exist(app, user):
    resp = app.test_client().post(
        '/api/users/999/subscribe',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 404
    assert 'User not found' in json.loads(resp.data)['message']


def test_subscribing_to_user_that_already_subscribed(app, user, session):
    user_2 = User(username='Bond')
    session.add(user_2)
    session.commit()
    user.subscribe(user_2)
    resp = app.test_client().post(
        '/api/users/{}/subscribe'.format(user_2.id),
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 409
    assert 'already subscribed to Bond' in json.loads(resp.data)['message']


def test_subscribing_to_a_user(app, user, session):
    user_2 = User()
    session.add(user_2)
    session.commit()
    resp = app.test_client().post(
        '/api/users/{}/subscribe'.format(user_2.id),
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 201
    expected_path = ('api/users/{}/subscriptions'.format(user.id))
    assert resp.headers['Location'].endswith(expected_path)


def test_unsubscibing_from_your_self(app, user):
    resp = app.test_client().delete(
        '/api/users/{}/unsubscribe'.format(user.id),
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 400
    assert 'Cannot unsubscribe from yourself' in \
        json.loads(resp.data)['message']


def test_unsubscribing_from_user_that_doesnt_exist(app, user):
    resp = app.test_client().delete(
        '/api/users/999/unsubscribe',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 404
    assert 'User not found' in json.loads(resp.data)['message']


def test_unsubscribing_from_user_that_didnt_subscribe(app, user, session):
    user_2 = User(username='Bond')
    session.add(user_2)
    session.commit()
    resp = app.test_client().delete(
        '/api/users/{}/unsubscribe'.format(user_2.id),
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 409
    assert 'You are not subscribed to Bond' in json.loads(resp.data)['message']


def test_unsubscribing_from_a_user(app, user, session):
    user_2 = User(username='Bond')
    session.add(user_2)
    session.commit()
    user.subscribe(user_2)
    resp = app.test_client().delete(
        '/api/users/{}/unsubscribe'.format(user_2.id),
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json')
    assert resp.status_code == 204
