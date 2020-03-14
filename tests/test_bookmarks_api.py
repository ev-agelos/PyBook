from datetime import datetime as dt, timedelta

import pytest
from flask import json

from bookmarks.models import Bookmark, Tag, Favourite, Vote


def test_getting_specific_bookmark_that_doesnt_exist(app, user, session):
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/1',
                     headers={'Authorization': 'token ' + user.auth_token})
    assert 'Bookmark not found' in json.loads(resp.data)['message']


def test_getting_specific_bookmark(app, user, session):
    b_1 = Bookmark(url='https://google.com')
    session.add(b_1)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/{}'.format(b_1.id),
                     headers={'Authorization': 'token ' + user.auth_token})
    assert json.loads(resp.data)['id'] == '/api/bookmarks/1'


def test_getting_latest_bookmarks_by_default(app, user, session):
    b_1 = Bookmark(id=1, created_on=dt.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/',
                     headers={'Authorization': 'token ' + user.auth_token})
    b_1_, b_2_ = json.loads(resp.data)['bookmarks']
    assert b_1_['id'] == '/api/bookmarks/2'
    assert b_2_['id'] == '/api/bookmarks/1'


@pytest.mark.parametrize('sort,order', [('date', [2, 1]), ('-date', [1, 2])])
def test_getting_bookmarks_sorted_by_date(app, user, session, sort, order):
    b_1 = Bookmark(id=1, created_on=dt.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/?sort=' + sort,
                     headers={'Authorization': 'token ' + user.auth_token})
    b_1_, b_2_ = json.loads(resp.data)['bookmarks']
    assert b_1_['id'] == '/api/bookmarks/' + str(order[0])
    assert b_2_['id'] == '/api/bookmarks/' + str(order[1])


@pytest.mark.parametrize('sort,order', [('rating', [2, 1]),
                                        ('-rating', [1, 2])])
def test_getting_bookmarks_sorted_by_rating(app, user, session, sort, order):
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, rating=1))
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/?sort=' + sort,
                     headers={'Authorization': 'token ' + user.auth_token})
    b_1_, b_2_ = json.loads(resp.data)['bookmarks']
    assert b_1_['id'] == '/api/bookmarks/' + str(order[0])
    assert b_2_['id'] == '/api/bookmarks/' + str(order[1])


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
        resp = c.get('/api/bookmarks/?tag=' + tag,
                     headers={'Authorization': 'token ' + user.auth_token})
    bookmarks = [item['id'] for item in json.loads(resp.data)['bookmarks']]
    assert bookmarks == ['/api/bookmarks/' + str(id) for id in expect]


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
        resp = c.get('/api/bookmarks/?tag=a_tag&sort=-rating',
                     headers={'Authorization': 'token ' + user.auth_token})
    ids = [item['id'] for item in json.loads(resp.data)['bookmarks']]
    assert ids == ['/api/bookmarks/2', '/api/bookmarks/1']


def test_adding_bookmark_with_invalid_form(app, user):
    resp = app.test_client().post(
        '/api/bookmarks/',
        headers={'Authorization': 'token ' + user.auth_token}, data={})
    assert resp.status_code == 400
    assert 'invalid data' in json.loads(resp.data)['message']


def test_adding_bookmark_that_already_exists(app, session, user):
    b_1 = Bookmark(url='http://test.com')
    session.add(b_1)
    session.commit()
    resp = app.test_client().post(
        '/api/bookmarks/',
        headers={'Authorization': 'token ' + user.auth_token},
        data={'url': 'http://test.com', 'title': 'a_title'})
    assert resp.status_code == 409
    assert 'bookmark already exists' in json.loads(resp.data)['message']


@pytest.mark.parametrize('input_,expect', [
    ({'tags-0': ''}, 'uncategorized'),
    ({'tags-0': 'a_tag'}, 'a_tag')])
def test_adding_bookmark_with_tag(app, session, user, input_, expect):
    data = dict(url='http://test.com', title='a_title', **input_)
    with app.test_client() as c:
        resp = c.post('/api/bookmarks/',
                    headers={'Authorization': 'token ' + user.auth_token},
                    # the default tag 'uncategorized' is being used
                    data=data)
    assert resp.status_code == 201
    assert session.query(Tag).one().name == expect
    assert '/bookmarks/1' in resp.headers['Location']


def test_updating_bookmark_when_doesnt_exist(app, user):
    resp = app.test_client().put(
        '/api/bookmarks/999',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'does not exist' in json.loads(resp.data)['message']


def test_updating_bookmark_with_bad_form_data(app, user, session):
    b_1 = Bookmark(url='http://test.com')
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'url': 'http//'})
    assert resp.status_code == 400
    assert 'invalid data' in json.loads(resp.data)['message']


def test_updating_bookmark_with_url_that_exists(app, user, session):
    b_1 = Bookmark(url='http://test.com')
    b_2 = Bookmark(url='http://test2.com')
    session.add(b_1)
    session.add(b_2)
    session.commit()
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'url': b_2.url})
    assert resp.status_code == 409
    assert 'url already exists' in json.loads(resp.data)['message']


def test_updating_bookmark_with_tag_that_doesnt_exist(app, user, session):
    t_1 = Tag(name='existing_tag')
    b_1 = Bookmark(url='http://test.com', tags=[t_1])
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'tags-0': 'new_tag'})
    assert resp.status_code == 200
    assert session.query(Tag).one().name == 'new_tag'


def test_updating_bookmark_with_tag_that_exists(app, user, session):
    t_1 = Tag(name='old_tag')
    b_1 = Bookmark(url='http://test.com', tags=[t_1])
    t_2 = Tag(name='new_tag')
    session.add(b_1)
    session.add(t_2)
    session.commit()
    assert Bookmark.query.one().tags == [t_1]
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'tags-0': 'new_tag'})
    assert resp.status_code == 200
    assert Tag.query.one().name == 'new_tag'


def test_updating_bookmark_with_new_title(app, user, session):
    b_1 = Bookmark(url='http://test.com', title='A bookmark title')
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'title': 'new title'})
    assert resp.status_code == 200
    assert session.query(Bookmark).one().title == 'new title'


def test_updating_bookmark_by_changing_all_its_info(app, user, session):
    t_1 = Tag(name='tag A')
    b_1 = Bookmark(url='http://test.com', tags=[t_1], title='title A')
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'url': 'http://test2.com', 'tags-0': 'tag B',
              'title': 'title B'})
    assert resp.status_code == 200
    assert json.loads(resp.data)['message'] == 'Bookmark updated'
    bookmark = session.query(Bookmark).one()
    assert bookmark.url == 'http://test2.com'
    assert bookmark.title == 'title B'
    assert len(bookmark.tags) == 1
    assert bookmark.tags[0].name == 'tag b'


def test_deleting_bookmark_that_doesnt_exist(app, user):
    resp = app.test_client().delete(
        '/api/bookmarks/1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'not found' in json.loads(resp.data)['message']


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
        '/api/bookmarks/' + str(b_1.id),
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
        '/api/bookmarks/' + str(b_1.id),
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
        '/api/bookmarks/' + str(b_1.id),
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
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 204
    assert session.query(Vote).scalar() is None


def test_saving_bookmark_that_doesnt_exist(app, user, session):
    resp = app.test_client().post(
        '/api/favourites/',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'bookmark_id': 999}
    )
    assert resp.status_code == 404
    assert 'bookmark not found' in json.loads(resp.data)['message']


def test_saving_bookmark_that_is_already_saved(app, user, session):
    b_1 = Bookmark(id=1, url='http://test.com', title='a_title',
                   user_id=user.id)
    f_1 = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(b_1)
    session.add(f_1)
    session.commit()
    resp = app.test_client().post(
        '/api/favourites/',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'bookmark_id': b_1.id}
    )
    assert resp.status_code == 409
    assert 'already saved' in json.loads(resp.data)['message']


def test_saving_bookmark_that_exists(app, user, session):
    b_1 = Bookmark(id=1, user_id=user.id)
    session.add(b_1)
    session.commit()
    resp = app.test_client().post(
        '/api/favourites/',
        headers={'Authorization': 'token ' + user.auth_token},
        json={'bookmark_id': b_1.id}
    )
    assert resp.status_code == 201
    assert session.query(Favourite).filter_by(bookmark_id=b_1.id,
                                              user_id=user.id).one()


def test_unsaving_bookmark_that_doesnt_exist(app, user, session):
    resp = app.test_client().delete(
        '/api/favourites/999',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'bookmark not found' in json.loads(resp.data)['message']


def test_unsaving_bookmark_where_save_doesnt_exist(app, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    session.commit()
    resp = app.test_client().delete(
        '/api/favourites/1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404
    assert 'save not found' in json.loads(resp.data)['message']


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
        '/api/favourites/1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 204
    assert favourite_query.scalar() is None


def test_getting_bookmark_votes_when_bookmark_doesnt_exist(app, user):
    resp = app.test_client().get(
        '/api/votes/?bookmark_id=999',
        headers={'Authorization': 'token ' + user.auth_token}
    )
    assert resp.status_code == 404
    assert 'not found' in json.loads(resp.data)['message']


def test_getting_bookmark_votes_filtering_by_bookmark_id(app, user, session):
    b_1 = Bookmark(id=1)
    vote_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    vote_2 = Vote(bookmark_id=b_1.id, user_id=user.id+1, direction=False)
    session.add(b_1)
    session.add(vote_1)
    session.add(vote_2)
    session.commit()
    resp = app.test_client().get(
        '/api/votes/?bookmark_id=1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 200
    votes = json.loads(resp.data)['votes']
    assert len(votes) == 1


def test_new_vote_with_bad_data(app, user):
    resp = app.test_client().post(
        '/api/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': 0}))
    assert resp.status_code == 400
    assert 'invalid data' in json.loads(resp.data)['message']


def test_updating_vote_with_direction_that_doesnt_exist(app, user, session):
    b_1 = Bookmark(id=1)
    vote = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(vote)
    session.commit()
    resp = app.test_client().put(
        f'/api/votes/{vote.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': 0}))
    assert resp.status_code == 400
    assert 'invalid data' in json.loads(resp.data)['message']


def test_new_vote_when_bookmark_id_doesnt_exist(app, user):
    resp = app.test_client().post(
        '/api/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': 1, 'bookmark_id': 1}))
    assert resp.status_code == 404
    assert 'not found' in json.loads(resp.data)['message']


def test_new_vote_when_vote_exists_for_the_given_bookmark(app, user, session):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = app.test_client().post(
        '/api/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': 1, 'bookmark_id': 1}))
    assert resp.status_code == 409
    assert 'already exists' in json.loads(resp.data)['message']


def test_new_vote(app, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    session.commit()
    resp = app.test_client().post(
        '/api/votes/',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': 1, 'bookmark_id': 1}))
    vote = Vote.query.filter_by(bookmark_id=b_1.id, user_id=user.id).one()
    assert resp.status_code == 201
    assert '/api/votes/{}'.format(vote.id) in \
        resp.headers['Location']
    assert vote.direction == True


def test_updating_vote_that_doesnt_exist(app, user, session):
    resp = app.test_client().put(
        '/api/votes/1',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': 1}))
    assert resp.status_code == 404
    assert 'not found' in json.loads(resp.data)['message']


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
        f'/api/votes/{v_1.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': vote_for}))
    assert resp.status_code == 409
    assert 'voted with {} already'.format(msg) in \
        json.loads(resp.data)['message']


@pytest.mark.parametrize('direction,vote_for', [(False, 1), (True, -1)])
def test_updating_vote(app, user, session, direction, vote_for):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=direction)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = app.test_client().put(
        f'/api/votes/{v_1.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json',
        data=json.dumps({'vote': vote_for}))
    assert resp.status_code == 200
    vote = Vote.query.filter_by(user_id=user.id, bookmark_id=b_1.id).one()
    assert vote.direction == (not direction)  # opposite than what it was


def test_deleting_vote_when_doesnt_exist(app, user):
    resp = app.test_client().delete(
        '/api/votes/1',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json'
    )
    assert resp.status_code == 404
    assert json.loads(resp.data)['message'] == 'vote not found'


def test_deleting_users_vote(app, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    vote = Vote(bookmark_id=1, user_id=user.id)
    session.add(vote)
    session.commit()
    resp = app.test_client().delete(
        f'/api/votes/{vote.id}',
        headers={'Authorization': 'token ' + user.auth_token},
        content_type='application/json'
    )
    assert resp.status_code == 204
    assert Vote.query.all() == []
