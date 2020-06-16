from flask import json

from bookmarks.users.models import User, UserSchema
from bookmarks.api.schemas import SubscriptionsSchema, VoteSchema, FavouriteSchema
from bookmarks.models import Bookmark, Vote, Favourite


def test_getting_all_users(app, api, user):
    resp = api.get('/users/')
    with app.test_request_context():
        users_json = UserSchema(many=True).dump([user])
    assert resp.get_json()['users'] == users_json


def test_getting_self_user(app, api, user):
    resp = api.get('/users/1')
    with app.test_request_context():
        user_json = UserSchema().dump(user)
    assert resp.get_json() == user_json


def test_getting_different_user(app, api, user, session):
    user_9 = User(id=9)
    session.add(user_9)
    session.commit()
    resp = api.get(f'/users/{user_9.id}')
    with app.test_request_context():
        user_json = UserSchema().dump(user_9)
    assert resp.get_json() == user_json


def test_getting_one_user_that_doesnt_exist(api, user):
    resp = api.get('/users/999')
    assert resp.status_code == 404
    assert 'User not found' in resp.get_json()['message']


def test_delete_self_user(api, user, session):
    resp = api.delete('/users/1')
    assert resp.status_code == 204
    assert User.query.get(user.id) is None


def test_delete_different_user(api, user, session):
    resp = api.delete('/users/999')
    assert resp.status_code == 403


def test_delete_user_deletes_his_favourites(api, user, session):
    favourite = Favourite(user_id=user.id, bookmark_id=999)
    session.add(favourite)
    session.commit()
    api.delete('/users/1')
    assert Favourite.query.filter_by(user_id=user.id).scalar() is None


def test_get_vote_from_different_user(api, user, session):
    vote = Vote(user_id=user.id + 1, bookmark_id=1, direction=False)
    session.add(vote)
    session.commit()

    resp = api.get(f'/votes/{vote.id}')
    assert resp.status_code == 403


def test_get_user_votes(api, user, session):
    b_1 = Bookmark(id=1)
    vote = Vote(user_id=user.id, bookmark_id=b_1.id, direction=False)
    session.add(vote)
    session.add(b_1)
    session.commit()
    resp = api.get('/votes/')
    assert resp.status_code == 200
    resp_votes = resp.get_json()
    assert resp_votes == VoteSchema(many=True).dump([vote])


def test_get_user_favourites(api, user, session):
    b_1 = Bookmark(id=1)
    favourite = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(favourite)
    session.add(b_1)
    session.commit()
    resp = api.get('/favourites/')
    assert resp.status_code == 200
    resp_favourites = resp.get_json()
    assert resp_favourites == FavouriteSchema(many=True).dump([favourite])


def test_get_subscribers(api, user, session):
    user_2 = User()
    session.add(user_2)
    session.commit()
    user_2.subscribe(user)
    resp = api.get('/subscriptions/?mySubscribers=true')
    assert resp.status_code == 200
    resp_subscribers = resp.get_json()
    assert resp_subscribers == SubscriptionsSchema(many=True).dump([user_2])


def test_get_subscriptions(api, user, session):
    user_2 = User()
    session.add(user_2)
    session.commit()
    user.subscribe(user_2)
    resp = api.get('/subscriptions/')
    assert resp.status_code == 200
    subscriptions = resp.get_json()
    assert subscriptions == SubscriptionsSchema(many=True).dump([user_2])


def test_subscribing_to_yourself(api, user):
    resp = api.post('/subscriptions/', json={'user_id': user.id})
    assert resp.status_code == 409
    assert 'Cannot subscribe to yourself' in resp.get_json()['message']


def test_subscribing_to_user_that_doesnt_exist(api, user):
    resp = api.post('/subscriptions/', json={'user_id': 999})
    assert resp.status_code == 409
    assert 'User not found' in resp.get_json()['message']


def test_subscribing_to_user_that_already_subscribed(api, user, session):
    user_2 = User(username='Bond')
    session.add(user_2)
    session.commit()
    user.subscribe(user_2)
    resp = api.post('/subscriptions/', json={'user_id': user_2.id})
    assert resp.status_code == 409
    assert 'Subscription already exists' in resp.get_json()['message']


def test_subscribing_to_a_user(api, user, session):
    user_2 = User()
    session.add(user_2)
    session.commit()
    resp = api.post('/subscriptions/', json={'user_id': user_2.id})
    assert resp.status_code == 204


def test_unsubscibing_from_your_self(api, user):
    resp = api.delete(f'/subscriptions/{user.id}')
    assert resp.status_code == 409
    assert 'Cannot unsubscribe from yourself' in resp.get_json()['message']


def test_unsubscribing_from_user_that_doesnt_exist(api, user):
    resp = api.delete('/subscriptions/999')
    assert resp.status_code == 409
    assert 'Subscription not found' in resp.get_json()['message']


def test_unsubscribing_from_user_that_didnt_subscribe(api, user, session):
    user_2 = User(username='Bond')
    session.add(user_2)
    session.commit()
    resp = api.delete(f'/subscriptions/{user_2.id}')
    assert resp.status_code == 409
    assert 'Subscription not found' in resp.get_json()['message']


def test_unsubscribing_from_a_user(api, user, session):
    user_2 = User(username='Bond')
    session.add(user_2)
    session.commit()
    user.subscribe(user_2)
    resp = api.delete(f'/subscriptions/{user_2.id}')
    assert resp.status_code == 204
