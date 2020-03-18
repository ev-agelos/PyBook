from datetime import datetime as dt, timedelta

import pytest
from flask import json

from bookmarks.models import Bookmark, Tag, Favourite, Vote


def test_getting_specific_bookmark_that_doesnt_exist(app, user, session):
    with app.test_client() as c:
        resp = c.get('/api/v1/bookmarks/1',
                     headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404


def test_getting_specific_bookmark(app, user, session):
    b_1 = Bookmark(url='https://google.com')
    session.add(b_1)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/v1/bookmarks/{}'.format(b_1.id),
                     headers={'Authorization': 'token ' + user.auth_token})
    assert resp.json['id'] == b_1.id


def test_getting_latest_bookmarks_by_default(app, user, session):
    b_1 = Bookmark(id=1, created_on=dt.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/v1/bookmarks/',
                     headers={'Authorization': 'token ' + user.auth_token})
    resp_ids = [b['id'] for b in resp.json]
    assert sorted(resp_ids) == sorted([b_1.id, b_2.id])


@pytest.mark.parametrize('sort,order', [('date', [2, 1]), ('-date', [1, 2])])
def test_getting_bookmarks_sorted_by_date(app, user, session, sort, order):
    b_1 = Bookmark(id=1, created_on=dt.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/v1/bookmarks/?sort=' + sort,
                     headers={'Authorization': 'token ' + user.auth_token})
    ids = [b['id'] for b in resp.json]
    assert ids == order


@pytest.mark.parametrize('sort,order', [
    ('rating', [2, 1]),
    ('-rating', [1, 2])
])
def test_getting_bookmarks_sorted_by_rating(app, user, session, sort, order):
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, rating=1))
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/v1/bookmarks/?sort=' + sort,
                     headers={'Authorization': 'token ' + user.auth_token})
    ids = [b['id'] for b in resp.json]
    assert ids == order


@pytest.mark.parametrize('tag,expect', [
    ('a_tag', [2]),
    ('b_tag', [])
])
def test_getting_bookmarks_by_tag(app, user, session, tag, expect):
    t_1 = Tag(name='a_tag')
    session.add(t_1)
    session.commit()
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, tags=[t_1]))
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/v1/bookmarks/?tag=' + tag,
                     headers={'Authorization': 'token ' + user.auth_token})
    ids = [b['id'] for b in resp.json]
    assert sorted(ids) == sorted(expect)


def test_getting_sorted_bookmarks_and_by_tag(app, user, session):
    t_1 = Tag(name='a_tag')
    session.add(t_1)
    session.commit()
    b_1 = Bookmark(id=3)
    b_2 = Bookmark(id=2, tags=[t_1])
    b_3 = Bookmark(id=1, tags=[t_1], rating=1)
    session.add(b_1)
    session.add(b_2)
    session.add(b_3)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/v1/bookmarks/?tag=a_tag&sort=-rating',
                     headers={'Authorization': 'token ' + user.auth_token})
    ids = [b['id'] for b in resp.json]
    assert ids == [b_2.id, b_3.id]


def test_adding_bookmark_with_missing_data(app, user):
    resp = app.test_client().post(
        '/api/v1/bookmarks/',
        headers={'Authorization': 'token ' + user.auth_token}, json={})
    assert resp.status_code == 422 and 'errors' in resp.json


def test_adding_bookmark_that_already_exists(app, session, user):
    b_1 = Bookmark(url='http://test.com')
    session.add(b_1)
    session.commit()
    resp = app.test_client().post(
        '/api/v1/bookmarks/',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'url': 'http://test.com', 'title': 'a'*10}
    )
    assert resp.status_code == 409 and 'Url already exists' in resp.json['message']


@pytest.mark.parametrize('input_,expect', [
    ({}, 'uncategorized'),  # default tag is uncategorized
    ({'tags': 'a_tag'}, 'a_tag')])
def test_adding_bookmark_with_tag(app, session, user, input_, expect):
    data = dict(url='http://test.com', title='a'*10, **input_)
    with app.test_client() as c:
        resp = c.post(
            '/api/v1/bookmarks/',
            headers={'Authorization': 'token ' + user.auth_token},
            json=data
        )
    assert resp.status_code == 201
    assert session.query(Tag).one().name == expect
    assert '/bookmarks/1' in resp.headers['Location']


def test_updating_bookmark_when_doesnt_exist(app, user):
    resp = app.test_client().put(
        '/api/v1/bookmarks/999',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'Bookmark not found' in resp.json['message']


def test_updating_bookmark_with_invalid_url(app, user, session):
    b_1 = Bookmark(url='http://test.com')
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        '/api/v1/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        json={'url': 'http//'}
    )
    assert resp.status_code == 422 and \
        resp.json['errors']['url'] == ['Not a valid URL.']


def test_updating_bookmark_with_url_that_exists(app, user, session):
    b_1 = Bookmark(url='http://test.com')
    b_2 = Bookmark(url='http://test2.com')
    session.add(b_1)
    session.add(b_2)
    session.commit()
    resp = app.test_client().put(
        '/api/v1/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        json={'url': b_2.url})
    assert resp.status_code == 409
    assert 'url already exists' in resp.json['message']


def test_updating_bookmark_with_tag_that_doesnt_exist(app, user, session):
    b_1 = Bookmark(url='http://test.com', tags=[Tag(name='existing_tag')])
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        f'/api/v1/bookmarks/{b_1.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'tags': 'new_tag'}
    )
    assert resp.status_code == 200 and Tag.query.one().name == 'new_tag'


def test_updating_bookmark_with_existing_tag(app, user, session):
    b_1 = Bookmark(url='http://test.com', tags=[Tag(name='old_tag')])
    session.add(b_1)
    session.add(Tag(name='new_tag'))
    session.commit()
    resp = app.test_client().put(
        f'/api/v1/bookmarks/{b_1.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'tags': 'new_tag'}
    )
    assert resp.status_code == 200 and Tag.query.one().name == 'new_tag'


def test_updating_bookmark_with_new_title(app, user, session):
    b_1 = Bookmark(url='http://test.com', title='A bookmark title')
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        f'/api/v1/bookmarks/{b_1.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'title': 'a new title'}
    )
    assert resp.json['title'] == 'a new title'


def test_updating_bookmark_changing_all_its_data(app, user, session):
    t_1 = Tag(name='tag A')
    b_1 = Bookmark(url='http://test.com', tags=[t_1], title='title A')
    session.add(b_1)
    session.commit()
    app.test_client().put(
        '/api/v1/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        json={'url': 'http://test2.com', 'tags': 'tag B', 'title': 'B'*10}
    )
    b = session.query(Bookmark).one()
    assert b.url == 'http://test2.com' and b.title == 'B'*10 \
        and len(b.tags) == 1 and b.tags[0].name == 'tag b'


def test_deleting_bookmark_that_doesnt_exist(app, user):
    resp = app.test_client().delete(
        '/api/v1/bookmarks/1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'not found' in resp.json['message']


@pytest.mark.parametrize('user_id,status', [
    (999, 403),  # does not belong to user
    (1, 204)  # user's bookmark
])
def test_deleting_bookmark(app, user, session, user_id, status):
    t_1 = Tag(name='a_tag')
    b_1 = Bookmark(url='http://test.com', title='title A', user_id=user_id,
                   tags=[t_1])
    session.add(b_1)
    session.commit()
    resp = app.test_client().delete(
        '/api/v1/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == status


def test_deleting_bookmark_deletes_associated_tag(app, user, session):
    t_1 = Tag(name='a_tag')
    b_1 = Bookmark(url='http://test.com', title='title A', user_id=user.id,
                   tags=[t_1])
    session.add(b_1)
    session.commit()
    assert session.query(Tag).one()
    resp = app.test_client().delete(
        '/api/v1/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 204
    assert session.query(Tag).scalar() is None


def test_deleting_bookmark_deletes_associated_saves(app, user, session):
    b_1 = Bookmark(id=1, url='http://test.com', title='title A',
                   user_id=user.id)
    f_1 = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(b_1)
    session.add(f_1)
    session.commit()
    assert session.query(Favourite).one()
    resp = app.test_client().delete(
        '/api/v1/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 204
    assert session.query(Favourite).scalar() is None


def test_deleting_bookmark_deletes_associated_votes(app, user, session):
    b_1 = Bookmark(id=1, url='http://test.com', title='title A',
                   user_id=user.id)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    assert session.query(Vote).one()
    resp = app.test_client().delete(
        '/api/v1/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 204
    assert session.query(Vote).scalar() is None


def test_saving_bookmark_that_doesnt_exist(app, user, session):
    resp = app.test_client().post(
        '/api/v1/favourites/',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'bookmark_id': 999}
    )
    assert resp.status_code == 404
    assert 'bookmark not found' in resp.json['message']


def test_saving_bookmark_that_is_already_saved(app, user, session):
    b_1 = Bookmark(id=1, url='http://test.com', title='a_title',
                   user_id=user.id)
    f_1 = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(b_1)
    session.add(f_1)
    session.commit()
    resp = app.test_client().post(
        '/api/v1/favourites/',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'bookmark_id': b_1.id}
    )
    assert resp.status_code == 409
    assert 'already saved' in resp.json['message']


def test_saving_bookmark_that_exists(app, user, session):
    b_1 = Bookmark(id=1, user_id=user.id)
    session.add(b_1)
    session.commit()
    resp = app.test_client().post(
        '/api/v1/favourites/',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'bookmark_id': b_1.id}
    )
    assert resp.status_code == 201
    assert session.query(Favourite).filter_by(bookmark_id=b_1.id,
                                              user_id=user.id).one()


def test_unsaving_bookmark_that_doesnt_exist(app, user, session):
    resp = app.test_client().delete(
        '/api/v1/favourites/999',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'bookmark not found' in resp.json['message']


def test_unsaving_bookmark_where_save_doesnt_exist(app, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    session.commit()
    resp = app.test_client().delete(
        '/api/v1/favourites/1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'save not found' in resp.json['message']


def test_unsaving_bookmark(app, user, session):
    b_1 = Bookmark(id=1)
    f_1 = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(b_1)
    session.add(f_1)
    session.commit()
    favourite_query = session.query(Favourite).filter_by(user_id=user.id,
                                                         bookmark_id=b_1.id)
    assert favourite_query.one()
    resp = app.test_client().delete(
        '/api/v1/favourites/1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 204
    assert favourite_query.scalar() is None


def test_getting_bookmark_votes_when_bookmark_doesnt_exist(app, user):
    resp = app.test_client().get(
        '/api/v1/votes/?bookmark_id=999',
        headers={'Authorization': 'token ' + user.auth_token}
    )
    assert resp.status_code == 404
    assert 'not found' in resp.json['message']


def test_getting_bookmark_votes_filtering_by_bookmark_id(app, user, session):
    b_1 = Bookmark(id=1)
    vote_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    vote_2 = Vote(bookmark_id=b_1.id, user_id=user.id+1, direction=False)
    session.add(b_1)
    session.add(vote_1)
    session.add(vote_2)
    session.commit()
    resp = app.test_client().get(
        '/api/v1/votes/?bookmark_id=1',
        headers={'Authorization': 'token ' + user.auth_token}
    )
    assert resp.status_code == 200 and len(resp.json) == 1


def test_new_vote_with_bad_data(app, user):
    resp = app.test_client().post(
        '/api/v1/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': 0}
    )
    assert resp.status_code == 400
    assert 'invalid data' in resp.json['message']


def test_updating_vote_with_direction_that_doesnt_exist(app, user, session):
    b_1 = Bookmark(id=1)
    vote = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(vote)
    session.commit()
    resp = app.test_client().put(
        f'/api/v1/votes/{vote.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': 0}
    )
    assert resp.status_code == 400
    assert 'invalid data' in resp.json['message']


def test_new_vote_when_bookmark_id_doesnt_exist(app, user):
    resp = app.test_client().post(
        '/api/v1/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': 1, 'bookmark_id': 1}
    )
    assert resp.status_code == 404
    assert 'not found' in resp.json['message']


def test_new_vote_when_vote_exists_for_the_given_bookmark(app, user, session):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = app.test_client().post(
        '/api/v1/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': 1, 'bookmark_id': 1}
    )
    assert resp.status_code == 409
    assert 'already exists' in resp.json['message']


def test_new_vote(app, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    session.commit()
    resp = app.test_client().post(
        '/api/v1/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': 1, 'bookmark_id': 1}
    )
    vote = Vote.query.filter_by(bookmark_id=b_1.id, user_id=user.id).one()
    assert resp.status_code == 201
    assert '/api/v1/votes/{}'.format(vote.id) in \
        resp.headers['Location']
    assert vote.direction == True


def test_updating_vote_that_doesnt_exist(app, user, session):
    resp = app.test_client().put(
        '/api/v1/votes/1',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': 1}
    )
    assert resp.status_code == 404
    assert 'not found' in resp.json['message']


@pytest.mark.parametrize('direction,vote_for,msg', [
    (True, 1, '+1'),
    (False, -1, '-1')
])
def test_updating_vote_for_bookmark_with_same_vote(app, user, session,
                                                   direction, vote_for, msg):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=direction)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = app.test_client().put(
        f'/api/v1/votes/{v_1.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': vote_for}
    )
    assert resp.status_code == 409
    assert 'voted with {} already'.format(msg) in \
        resp.json['message']


@pytest.mark.parametrize('direction,vote_for', [(False, 1), (True, -1)])
def test_updating_vote(app, user, session, direction, vote_for):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=direction)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = app.test_client().put(
        f'/api/v1/votes/{v_1.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        json={'vote': vote_for}
    )
    assert resp.status_code == 200
    vote = Vote.query.filter_by(user_id=user.id, bookmark_id=b_1.id).one()
    assert vote.direction == (not direction)  # opposite than what it was


def test_deleting_vote_when_doesnt_exist(app, user):
    resp = app.test_client().delete(
        '/api/v1/votes/1',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json'
    )
    assert resp.status_code == 404
    assert resp.json['message'] == 'vote not found'


def test_deleting_users_vote(app, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    vote = Vote(bookmark_id=1, user_id=user.id)
    session.add(vote)
    session.commit()
    resp = app.test_client().delete(
        f'/api/v1/votes/{vote.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json'
    )
    assert resp.status_code == 204
    assert Vote.query.all() == []
