"""The logic around bookmarks so both api and regular views share."""


from flask import g
from sqlalchemy.sql.expression import asc, desc

from bookmarks import db
from bookmarks.views import utils
from .models import Bookmark, Tag, tags_bookmarks, Vote, Favourite

SORTS = {'date': desc(Bookmark.created_on), '-date': asc(Bookmark.created_on),
         'rating': desc(Bookmark.rating), '-rating': asc(Bookmark.rating)}


def _get(args):
    """
    Return the query for all bookmarks.

    This function returns the query comparing to other functions because the
    regular view paginates the query where the api view applies schema in order
    to return the result in json.
    """
    query = Bookmark.query
    for tag in args.get('tag', []):
        query = query.filter(Tag.name == tag)
    if args.get('tag'):
        query = query.join(tags_bookmarks).join(Tag)
    query = query.order_by(SORTS[args['sort']])

    return query


def _post(data):
    """Add a new bookmark according to the given data."""
    bookmark = Bookmark(title=data['title'], url=data['url'],
                        user_id=g.user.id)
    for string in data['tags']:
        tag = Tag.query.filter_by(name=string.lower()).scalar()
        if tag is None:
            tag = Tag(name=string.lower())
            db.session.add(tag)
        bookmark.tags.append(tag)

    db.session.add(bookmark)
    db.session.commit()
    # TODO add method to bookmark's class
    utils.get_url_thumbnail(data['url'], bookmark.id)
    return bookmark.id


def _put(id, data):
    """Update bookmark with the given data."""
    bookmark = Bookmark.query.get(id)
    if 'url' in data and data['url'] != bookmark.url:
        # FIXME when url changes, should grab the new favicon/image
        bookmark.url = data['url']
    if 'title' in data and data['title'] != bookmark.title:
        bookmark.title = data['title']

    given_tags = {string.lower() for string in data.get('tags', [])}
    linked_tags = {tag.name: tag for tag in bookmark.tags}
    tags_to_del = set(linked_tags.keys()) - given_tags
    tags_to_add = given_tags - set(linked_tags.keys())
    if given_tags != set(linked_tags.keys()):
        for name in tags_to_del:  # un-link not given tags
            tag_to_del = linked_tags[name]
            if db.session.query(tags_bookmarks).filter_by(
                    tag_id=tag_to_del.id).count() == 1:
                db.session.delete(tag_to_del)
            bookmark.tags.remove(tag_to_del)

        existing = Tag.query.filter(Tag.name.in_(tags_to_add)).all()
        existing_tags = {tag.name: tag for tag in existing}
        for new_string in tags_to_add:  # link the given tags
            tag = existing_tags.get(new_string, Tag(name=new_string))
            bookmark.tags.append(tag)

    db.session.add(bookmark)
    db.session.commit()


def _delete(id):
    """Delete a bookmark."""
    bookmark = Bookmark.query.get(id)
    # Delete associated tags
    for tag in bookmark.tags:
        if db.session.query(tags_bookmarks).filter_by(
                tag_id=tag.id).count() == 1:
            db.session.delete(tag)
    db.session.delete(bookmark)
    db.session.commit()


def _save(bookmark_id):
    """Save a bookmark to user's listings."""
    favourite = Favourite(bookmark_id=bookmark_id, user_id=g.user.id)
    db.session.add(favourite)
    db.session.commit()
    return favourite.id


def _unsave(favourite):
    """Remove saved bookmark from user's listings."""
    db.session.delete(favourite)
    db.session.commit()


def _post_vote(bookmark, direction):
    """Create a new vote entry."""
    bookmark.rating += direction
    vote = Vote(user_id=g.user.id, bookmark_id=bookmark.id,
                direction=True if direction == 1 else False)
    db.session.add(bookmark)
    db.session.add(vote)
    db.session.commit()
    return vote.id


def _put_vote(vote_, direction):
    """Update an existing vote."""
    bookmark = Bookmark.query.get(vote_.bookmark_id)
    if vote_.direction is None:
        vote_.direction = {-1: False, 1: True}[direction]
        bookmark.rating += direction
    elif vote_.direction is True:
        vote_.direction = {-1: False, 1: None}[direction]
        bookmark.rating += -1 if direction == 1 else -2
    else:
        vote_.direction = {-1: None, 1: True}[direction]
        bookmark.rating += 1 if direction == -1 else 2
    db.session.add(vote_)
    db.session.add(bookmark)
    db.session.commit()


def _delete_vote(vote):
    """Delete an existing vote."""
    if vote.direction is not None:
        vote.bookmark.rating += -1 if vote.direction is True else 1
        db.session.add(vote.bookmark)
    db.session.delete(vote)
    db.session.commit()
