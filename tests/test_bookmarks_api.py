from datetime import datetime as dt, timedelta
from base64 import b64encode

import pytest
from flask import json, g

from bookmarks.models import Bookmark, Category


def test_getting_latest_bookmarks_by_default(app, user, session):
    b_1 = Bookmark(id=1, created_on=dt.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/',
                     headers={'Authorization': 'token '+ user.auth_token})
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


@pytest.mark.parametrize('category,expect', [
    ('a_category', [2]),
    ('b_category', [1, 2])  # Non existing category returns all bookmarks
])
def test_getting_bookmarks_by_category(app, user, session, category, expect):
    c_1 = Category(name='a_category')
    session.add(c_1)
    session.commit()
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, category=c_1))
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/?category=' + category,
                     headers={'Authorization': 'token ' + user.auth_token})
    bookmarks = [item['id'] for item in json.loads(resp.data)['bookmarks']]
    assert bookmarks == ['/api/bookmarks/' + str(id) for id in expect]


def test_getting_sorted_bookmarks_and_by_category(app, user, session):
    c_1 = Category(name='a_category')
    session.add(c_1)
    session.commit()
    b_1 = Bookmark(id=3)
    b_2 = Bookmark(id=2, category=c_1)
    b_3 = Bookmark(id=1, category=c_1, rating=1)
    session.add(b_1)
    session.add(b_2)
    session.add(b_3)
    session.commit()
    with app.test_client() as c:
        resp = c.get('/api/bookmarks/?category=a_category&sort=-rating',
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
    (None, 'uncategorized'),
    ('a_category', 'a_category')])
def test_adding_bookmark_with_category(app, session, user, input_, expect):
    with app.test_client() as c:
        resp = c.post('/api/bookmarks/',
                    headers={'Authorization': 'token ' + user.auth_token},
                    # the default category 'uncategorized' is being used
                    data={'url': 'http://test.com', 'title': 'a_title',
                          'category': input_})
    assert resp.status_code == 201
    assert session.query(Category).one().name == expect
    assert '/bookmarks/1' in resp.location


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


def test_updating_bookmark_with_category_that_doesnt_exist(app, user, session):
    c_1 = Category(name='existing_category')
    b_1 = Bookmark(url='http://test.com', category=c_1)
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'category': 'new_category'})
    assert resp.status_code == 200
    assert session.query(Bookmark).one().category.name == 'new_category'


def test_updating_bookmark_with_category_that_exists(app, user, session):
    c_1 = Category(name='old_category')
    c_2 = Category(name='new_category')
    b_1 = Bookmark(url='http://test.com', category=c_1)
    session.add(b_1)
    session.add(c_2)
    session.commit()
    assert session.query(Bookmark).one().category.name == 'old_category'
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'category': 'new_category'})
    assert resp.status_code == 200
    assert session.query(Bookmark).one().category.name == 'new_category'


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
    c_1 = Category(name='category A')
    b_1 = Bookmark(url='http://test.com', category=c_1, title='title A')
    session.add(b_1)
    session.commit()
    resp = app.test_client().put(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token},
        data={'url': 'http://test2.com', 'category': 'category B',
              'title': 'title B'})
    assert resp.status_code == 200
    assert json.loads(resp.data)['message'] == 'Bookmark updated'
    bookmark = session.query(Bookmark).one()
    assert bookmark.url == 'http://test2.com'
    assert bookmark.title == 'title B'
    assert bookmark.category.name == 'category b'  # name changes to lowercase


def test_deleting_bookmark_that_doesnt_exist(app, user):
    resp = app.test_client().delete(
        '/api/bookmarks/1',
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 404


@pytest.mark.parametrize('user_id,status', [
    (999, 403),  # does not exist to user
    (1, 204)  # user's bookmark
])
def test_deleting_bookmark(app, user, session, user_id, status):
    print("USER   ", user.id)
    c_1 = Category(name='a_category')
    b_1 = Bookmark(url='http://test.com', title='title A', user_id=user_id,
                   category=c_1)
    session.add(b_1)
    session.commit()
    resp = app.test_client().delete(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == status


def test_deleting_bookmark_deletes_category(app, user, session):
    c_1 = Category(name='a_category')
    b_1 = Bookmark(url='http://test.com', title='title A', user_id=user.id,
                   category=c_1)
    session.add(b_1)
    session.commit()
    assert session.query(Category).one()
    resp = app.test_client().delete(
        '/api/bookmarks/' + str(b_1.id),
        headers={'Authorization': 'token ' + user.auth_token})
    assert resp.status_code == 204
    assert session.query(Category).scalar() is None
