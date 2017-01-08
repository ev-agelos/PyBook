from datetime import datetime, timedelta

import pytest

from bookmarks import logic
from bookmarks.models import Bookmark, Category


def test_getting_latest_bookmarks_by_default(app, session):
    b_1, b_2 = Bookmark(), Bookmark()
    session.add(b_1)
    session.add(b_2)
    session.commit()
    with app.test_request_context('/api/bookmarks/'):
        bookmarks = logic._get().all()
    assert bookmarks == [b_1, b_2]


@pytest.mark.parametrize('sort,order', [('date', [2, 1]), ('-date', [1, 2])])
def test_getting_bookmarks_sorted_by_date(app, session, sort, order):
    b_1 = Bookmark(id=1, created_on=datetime.now())
    b_2 = Bookmark(id=2, created_on=b_1.created_on + timedelta(0, 1))
    session.add(b_1)
    session.add(b_2)
    session.commit()
    with app.test_request_context('/api/bookmarks/?sort=' + sort):
        bookmarks = logic._get().all()
    bookmark_ids = [bookmark.id for bookmark in bookmarks]
    assert bookmark_ids == order


@pytest.mark.parametrize('sort,order', [('rating', [2, 1]),
                                        ('-rating', [1, 2])])
def test_getting_bookmarks_sorted_by_rating(app, session, sort, order):
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, rating=1))
    session.commit()
    with app.test_request_context('/api/bookmarks/?sort=' + sort):
        bookmarks = logic._get().all()
    bookmark_ids = [bookmark.id for bookmark in bookmarks]
    assert bookmark_ids == order


@pytest.mark.parametrize('category,result', [
    ('a_category', [2]),
    ('b_category', [1, 2])  # Non existing category returns all bookmarks
])
def test_getting_bookmarks_by_category(app, session, category, result):
    c_1 = Category(name='a_category')
    session.add(c_1)
    session.commit()
    session.add(Bookmark(id=1))
    session.add(Bookmark(id=2, category=c_1))
    session.commit()
    with app.test_request_context('/api/bookmarks/?category=' + category):
        bookmarks = logic._get().all()
    bookmark_ids = [bookmark.id for bookmark in bookmarks]
    assert bookmark_ids == result


def test_getting_sorted_bookmarks_and_by_category(app, session):
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
    with app.test_request_context('/api/bookmarks/?category=a_category'
                                  '&sort=-rating'):
        bookmarks = logic._get().all()
    assert bookmarks == [b_2, b_3]
