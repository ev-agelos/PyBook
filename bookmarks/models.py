"""Create the database schema for the application."""


from bookmarks import db
from .schemas import (CategorySchema, BookmarkSchema, VoteSchema,
                      SaveBookmarkSchema)


class Category(db.Model):
    """Define column for bookmark categories."""

    __tablename__ = 'categories'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True, unique=True,
                     default='Uncategorized')

    def serialize(self):
        """Return object serialized according to it's schema."""
        schema = CategorySchema()
        return schema.dump(self)

    def __repr__(self):
        """Representation of a Category instance."""
        return '<Category {}>'.format(self.name)


class Bookmark(db.Model):
    """"Define columns for bookmarks table."""

    __tablename__ = 'bookmarks'

    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    url = db.Column(db.String, unique=True)
    rating = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    thumbnail = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('users._id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories._id'))

    def serialize(self):
        """Return object serialized according to it's schema."""
        schema = BookmarkSchema()
        return schema.dump(self)

    def __repr__(self):
        """Representation of a Bookmark instance."""
        return '<Bookmark {}>'.format(self.title)


class Vote(db.Model):
    """Define what each user voted for each bookmark."""

    __tablename__ = 'votes'

    _id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'))
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks._id'))

    def serialize(self):
        """Return object serialized according to it's schema."""
        schema = VoteSchema()
        return schema.dump(self)

    def __repr__(self):
        """Representation of a Vote instance."""
        return '<Vote {}>'.format(self.direction)


class SaveBookmark(db.Model):
    """Define what bookmarks each user saved."""

    __tablename__ = 'savebookmark'

    _id = db.Column(db.Integer, primary_key=True)
    is_saved = db.Column(db.Boolean, default=True)
    saved_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'))
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks._id'))

    def serialize(self):
        """Return object serialized according to it's schema."""
        schema = SaveBookmarkSchema()
        return schema.dump(self)

    def __repr__(self):
        """Representation of a SaveBookmark instance."""
        return '<SaveBookmark {}>'.format(self.saved_on)
