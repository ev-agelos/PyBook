from bookmarks.users.models import User
from bookmarks import bcrypt


def test_password_gets_hashed_when_being_set():
    """Testing the library method."""
    user = User(username='test user', password='123')
    assert bcrypt.check_password_hash(user.password, '123')


def test_plaintext_password_is_the_hashed_one():
    """Testing the class method."""
    user = User(username='test user', password='123')
    assert user.is_password_correct('123')


def test_user_object_representation():
    user = User(username='test user')
    assert repr(user) == '<User test user>'
