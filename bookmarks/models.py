"""Create the database schema for the application."""


from sqlalchemy.orm import backref
import arrow

from bookmarks import db


class Category(db.Model):
    """Define column for bookmark categories."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, default='Uncategorized')

    def __repr__(self):
        """Representation of a Category instance."""
        return '<Category {}>'.format(self.name)


class Bookmark(db.Model):
    """"Define columns for bookmarks table."""

    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    url = db.Column(db.String, unique=True)
    rating = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    thumbnail = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def get_human_time(self):
        """Humanize and return the created_on time."""
        return arrow.get(self.created_on).humanize()

    def __repr__(self):
        """Representation of a Bookmark instance."""
        return '<Bookmark {}>'.format(self.title)


class Vote(db.Model):
    """Define what each user voted for each bookmark."""

    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.id'))

    bookmark = db.relationship(Bookmark, backref=backref('vote',
                                                         uselist=False))
    def __repr__(self):
        """Representation of a Vote instance."""
        return '<Vote {}>'.format(self.direction)


class SaveBookmark(db.Model):
    """Define what bookmarks each user saved."""

    __tablename__ = 'savebookmark'

    id = db.Column(db.Integer, primary_key=True)
    is_saved = db.Column(db.Boolean, default=True)
    saved_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.id'))

    bookmark = db.relationship(Bookmark, backref=backref('saved',
                                                         uselist=False))

    def __repr__(self):
        """Representation of a SaveBookmark instance."""
        return '<SaveBookmark {}>'.format(self.saved_on)
