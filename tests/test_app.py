"""Tests for application."""


def test_something(app):
    """Just a basic test."""
    response = app.get('/')
    assert b"<title>Bookmarks</title>" in response.data
