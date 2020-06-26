from datetime import datetime as dt, timedelta

import pytest

from bookmarks.models import Bookmark, Tag, Favourite, Vote


def test_getting_specific_bookmark_that_doesnt_exist(api, user, session):
    resp = api.get('/bookmarks/1')
    assert resp.status_code == 404


def test_getting_specific_bookmark(api, user, session):
    b_1 = Bookmark(url='https://google.com')
    session.add(b_1)
    session.commit()
    resp = api.get(f'/bookmarks/{b_1.id}')
    assert resp.get_json()['id'] == b_1.id


def test_getting_latest_bookmarks_by_default(api, user, session):
    b_1 = Bookmark(id=1, created_on=dt.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    resp = api.get('/bookmarks/')
    resp_ids = [b['id'] for b in resp.get_json()]
    assert sorted(resp_ids) == sorted([b_1.id, b_2.id])


@pytest.mark.parametrize('sort,order', [('date', [2, 1]), ('-date', [1, 2])])
def test_getting_bookmarks_sorted_by_date(api, user, session, sort, order):
    b_1 = Bookmark(id=1, created_on=dt.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    resp = api.get(f'/bookmarks/?sort={sort}')
    ids = [b['id'] for b in resp.get_json()]
    assert ids == order


@pytest.mark.parametrize('sort,order', [
    ('rating', [2, 1]),
    ('-rating', [1, 2])
])
def test_getting_bookmarks_sorted_by_rating(api, user, session, sort, order):
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, rating=1))
    session.commit()
    resp = api.get(f'/bookmarks/?sort={sort}')
    ids = [b['id'] for b in resp.get_json()]
    assert ids == order


@pytest.mark.parametrize('tag,expect', [
    ('a_tag', [2]),
    ('b_tag', [])
])
def test_getting_bookmarks_by_tag(api, user, session, tag, expect):
    t_1 = Tag(name='a_tag')
    session.add(t_1)
    session.commit()
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, tags=[t_1]))
    session.commit()
    resp = api.get(f'/bookmarks/?tag={tag}')
    ids = [b['id'] for b in resp.get_json()]
    assert sorted(ids) == sorted(expect)


def test_getting_sorted_bookmarks_and_by_tag(api, user, session):
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
    resp = api.get('/bookmarks/?tag=a_tag&sort=-rating')
    ids = [b['id'] for b in resp.get_json()]
    assert ids == [b_2.id, b_3.id]


def test_adding_bookmark_with_missing_data(api, user):
    resp = api.post('/bookmarks/', json={})
    assert resp.status_code == 422 and 'errors' in resp.get_json()


def test_adding_bookmark_that_already_exists(api, session, user):
    b_1 = Bookmark(url='http://test.com')
    session.add(b_1)
    session.commit()
    resp = api.post('/bookmarks/',
                    json={'url': 'http://test.com', 'title': 'a'*10})
    assert resp.status_code == 409 and 'Url already exists' in resp.get_json()['message']


@pytest.mark.parametrize('input_,expect', [
    ({}, 'uncategorized'),  # default tag is uncategorized
    ({'tags': ['a_tag']}, 'a_tag')])
def test_adding_bookmark_with_tag(api, session, user, input_, expect):
    data = dict(url='http://test.com', title='a'*10, **input_)
    resp = api.post('/bookmarks/', json=data)
    assert resp.status_code == 201
    assert session.query(Tag).one().name == expect
    assert '/bookmarks/1' in resp.headers['location']


def test_updating_bookmark_when_doesnt_exist(api, user):
    resp = api.put('/bookmarks/999')
    assert resp.status_code == 404
    assert 'Bookmark not found' in resp.get_json()['message']


def test_updating_bookmark_with_invalid_url(api, user, session):
    b_1 = Bookmark(url='http://test.com')
    session.add(b_1)
    session.commit()
    resp = api.put(f'/bookmarks/{b_1.id}', json={'url': 'http//'})
    assert resp.status_code == 422 and \
        resp.get_json()['errors']['json']['url'] == ['Not a valid URL.']


def test_updating_bookmark_with_url_that_exists(api, user, session):
    b_1 = Bookmark(url='http://test.com')
    b_2 = Bookmark(url='http://test2.com')
    session.add(b_1)
    session.add(b_2)
    session.commit()
    resp = api.put(f'/bookmarks/{b_1.id}', json={'url': b_2.url})
    assert resp.status_code == 409
    assert 'url already exists' in resp.get_json()['message']


def test_updating_bookmark_with_tag_that_doesnt_exist(api, user, session):
    b_1 = Bookmark(url='http://test.com', tags=[Tag(name='existing_tag')])
    session.add(b_1)
    session.commit()
    resp = api.put(f'/bookmarks/{b_1.id}', json={'tags': ['new_tag']})
    assert resp.status_code == 204 and Tag.query.one().name == 'new_tag'


def test_updating_bookmark_with_existing_tag(api, user, session):
    b_1 = Bookmark(url='http://test.com', tags=[Tag(name='old_tag')])
    session.add(b_1)
    session.add(Tag(name='new_tag'))
    session.commit()
    resp = api.put(f'/bookmarks/{b_1.id}', json={'tags': ['new_tag']})
    assert resp.status_code == 204 and Tag.query.one().name == 'new_tag'


def test_updating_bookmark_with_new_title(api, user, session):
    b_1 = Bookmark(url='http://test.com', title='A bookmark title')
    session.add(b_1)
    session.commit()
    api.put(f'/bookmarks/{b_1.id}', json={'title': 'a new title'})
    assert api.get(f'/bookmarks/{b_1.id}').get_json()['title'] == 'a new title'


def test_updating_bookmark_changing_all_its_data(api, user, session):
    t_1 = Tag(name='tag A')
    b_1 = Bookmark(url='http://test.com', tags=[t_1], title='title A')
    session.add(b_1)
    session.commit()
    resp=api.put(f'/bookmarks/{b_1.id}',
            json={'url': 'http://test2.com', 'tags': ['tag B'], 'title': 'B'*10})
    b = session.query(Bookmark).one()
    assert b.url == 'http://test2.com' and b.title == 'B'*10 \
        and len(b.tags) == 1 and b.tags[0].name == 'tag b'


def test_deleting_bookmark_that_doesnt_exist(api, user):
    resp = api.delete('/bookmarks/1')
    assert resp.status_code == 404
    assert 'not found' in resp.get_json()['message']


@pytest.mark.parametrize('user_id,status', [
    (999, 403),  # does not belong to user
    (1, 204)  # user's bookmark
])
def test_deleting_bookmark(api, user, session, user_id, status):
    t_1 = Tag(name='a_tag')
    b_1 = Bookmark(url='http://test.com', title='title A', user_id=user_id,
                   tags=[t_1])
    session.add(b_1)
    session.commit()
    resp = api.delete(f'/bookmarks/{b_1.id}')
    assert resp.status_code == status


def test_deleting_bookmark_deletes_associated_tag(api, user, session):
    t_1 = Tag(name='a_tag')
    b_1 = Bookmark(url='http://test.com', title='title A', user_id=user.id,
                   tags=[t_1])
    session.add(b_1)
    session.commit()
    assert session.query(Tag).one()
    resp = api.delete(f'/bookmarks/{b_1.id}')
    assert resp.status_code == 204
    assert session.query(Tag).scalar() is None


def test_deleting_bookmark_deletes_associated_saves(api, user, session):
    b_1 = Bookmark(id=1, url='http://test.com', title='title A',
                   user_id=user.id)
    f_1 = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(b_1)
    session.add(f_1)
    session.commit()
    assert session.query(Favourite).one()
    resp = api.delete(f'/bookmarks/{b_1.id}')
    assert resp.status_code == 204
    assert session.query(Favourite).scalar() is None


def test_deleting_bookmark_deletes_associated_votes(api, user, session):
    b_1 = Bookmark(id=1, url='http://test.com', title='title A',
                   user_id=user.id)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    assert session.query(Vote).one()
    resp = api.delete(f'/bookmarks/{b_1.id}')
    assert resp.status_code == 204
    assert session.query(Vote).scalar() is None


def test_saving_bookmark_that_doesnt_exist(api, user, session):
    resp = api.post('/favourites/', json={'bookmark_id': 999})
    assert resp.status_code == 404
    assert 'bookmark not found' in resp.get_json()['message']


def test_saving_bookmark_that_is_already_saved(api, user, session):
    b_1 = Bookmark(id=1, url='http://test.com', title='a_title',
                   user_id=user.id)
    f_1 = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(b_1)
    session.add(f_1)
    session.commit()
    resp = api.post('/favourites/', json={'bookmark_id': b_1.id})
    assert resp.status_code == 409
    assert 'already saved' in resp.get_json()['message']


def test_saving_bookmark_that_exists(api, user, session):
    b_1 = Bookmark(id=1, user_id=user.id)
    session.add(b_1)
    session.commit()
    resp = api.post('/favourites/', json={'bookmark_id': b_1.id})
    assert resp.status_code == 201
    assert session.query(Favourite).filter_by(bookmark_id=b_1.id,
                                              user_id=user.id).one()


def test_unsaving_bookmark_that_doesnt_exist(api, user, session):
    resp = api.delete('/favourites/999')
    assert resp.status_code == 404
    assert 'Bookmark not found' in resp.get_json()['message']


def test_unsaving_bookmark_where_save_doesnt_exist(api, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    session.commit()
    resp = api.delete('/favourites/1')
    assert resp.status_code == 404
    assert 'Favourite not found' in resp.get_json()['message']


def test_unsaving_bookmark(api, user, session):
    b_1 = Bookmark(id=1)
    f_1 = Favourite(user_id=user.id, bookmark_id=b_1.id)
    session.add(b_1)
    session.add(f_1)
    session.commit()
    favourite_query = session.query(Favourite).filter_by(user_id=user.id,
                                                         bookmark_id=b_1.id)
    assert favourite_query.one()
    resp = api.delete('/favourites/1')
    assert resp.status_code == 204
    assert favourite_query.scalar() is None


def test_getting_bookmark_votes_when_bookmark_doesnt_exist(api, user):
    resp = api.get('/votes/?bookmark_id=999')
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_getting_bookmark_votes_filtering_by_bookmark_id(api, user, session):
    b_1 = Bookmark(id=1)
    vote_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    vote_2 = Vote(bookmark_id=b_1.id, user_id=user.id+1, direction=False)
    session.add(b_1)
    session.add(vote_1)
    session.add(vote_2)
    session.commit()
    resp = api.get('/votes/?bookmark_id=1')
    assert resp.status_code == 200 and len(resp.get_json()) == 1


def test_new_vote_with_bad_data(api, user):
    resp = api.post('/votes/', json={'direction': 0})
    assert resp.status_code == 422
    assert 'errors' in resp.get_json()


def test_updating_vote_with_direction_that_doesnt_exist(api, user, session):
    b_1 = Bookmark(id=1)
    vote = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(vote)
    session.commit()
    resp = api.put(f'/votes/{vote.id}', json={'direction': 0})
    assert resp.status_code == 422
    assert 'errors' in resp.get_json()


def test_new_vote_when_bookmark_id_doesnt_exist(api, user):
    resp = api.post('/votes/', json={'direction': 1, 'bookmark_id': 1})
    assert resp.status_code == 404
    assert 'not found' in resp.get_json()['message']


def test_new_vote_when_vote_exists_for_the_given_bookmark(api, user, session):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=True)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = api.post('/votes/', json={'direction': 1, 'bookmark_id': 1})
    assert resp.status_code == 409
    assert 'already exists' in resp.get_json()['message']


def test_new_vote(api, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    session.commit()
    resp = api.post('/votes/', json={'direction': 1, 'bookmark_id': 1})
    vote = Vote.query.filter_by(bookmark_id=b_1.id, user_id=user.id).one()
    assert resp.status_code == 201
    assert '/votes/{}'.format(vote.id) in \
        resp.headers['location']
    assert vote.direction is True


def test_updating_vote_that_doesnt_exist(api, user, session):
    resp = api.put('/votes/1', json={'direction': 1})
    assert resp.status_code == 404
    assert 'not found' in resp.get_json()['message']


@pytest.mark.parametrize('direction,vote_for,msg', [
    (True, 1, '+1'),
    (False, -1, '-1')
])
def test_updating_vote_for_bookmark_with_same_vote(api, user, session,
                                                   direction, vote_for, msg):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=direction)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = api.put(f'/votes/{v_1.id}', json={'direction': vote_for})
    assert resp.status_code == 204


@pytest.mark.parametrize('direction,vote_for', [(False, 1), (True, -1)])
def test_updating_vote(api, user, session, direction, vote_for):
    b_1 = Bookmark(id=1)
    v_1 = Vote(bookmark_id=b_1.id, user_id=user.id, direction=direction)
    session.add(b_1)
    session.add(v_1)
    session.commit()
    resp = api.put(f'/votes/{v_1.id}', json={'direction': vote_for})
    assert resp.status_code == 204
    vote = Vote.query.filter_by(user_id=user.id, bookmark_id=b_1.id).one()
    assert vote.direction == (not direction)  # opposite than what it was


def test_deleting_vote_when_doesnt_exist(api, user):
    resp = api.delete('/votes/1')
    assert resp.status_code == 404
    assert resp.get_json()['message'] == 'Vote not found'


def test_deleting_users_vote(api, user, session):
    b_1 = Bookmark(id=1)
    session.add(b_1)
    vote = Vote(bookmark_id=1, user_id=user.id)
    session.add(vote)
    session.commit()
    resp = api.delete(f'/votes/{vote.id}')
    assert resp.status_code == 204
    assert Vote.query.all() == []
