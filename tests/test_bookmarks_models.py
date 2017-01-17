from datetime import datetime

import pytest

from bookmarks.models import Tag, Bookmark, Vote, Favourite
from bookmarks.users.models import User


@pytest.mark.parametrize('model,expected', [
    (Tag(), '<Tag uncategorized>'),
    (Bookmark(title='Random Title'), '<Bookmark Random Title>'),
    (Vote(direction=True, user_id=1, bookmark_id=1), '<Vote True>'),
    (Favourite(saved_on=datetime(2016, 9, 25, 13, 34, 11), user_id=1,
               bookmark_id=1),
     '<Favourite 2016-09-25 13:34:11>')
])
def test_model_representations(model, expected, session):
    session.add(model)
    session.commit()
    assert repr(model) == expected


def test_getting_relative_bookmark_creation_time(session):
    bookmark = Bookmark()
    session.add(bookmark)
    session.commit()
    assert bookmark.get_human_time() == 'just now'
