"""Create the database schema for the application."""


import arrow

from bookmarks import db, ma


tags_bookmarks = db.Table(
    'tags_bookmarks',
    db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmarks.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Tag(db.Model):
    """Define column for bookmark tags."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, default='uncategorized')

    def __repr__(self):
        """Representation of a Tag instance."""
        return '<Tag {}>'.format(self.name)


class Bookmark(db.Model):
    """"Define columns for bookmarks table."""

    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50))
    url = db.Column(db.String, unique=True)
    rating = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    image = db.Column(db.String(50), nullable=True)

    tags = db.relationship('Tag', secondary=tags_bookmarks,
                           backref=db.backref('bookmarks', lazy='dynamic'))
    votes = db.relationship('Vote', backref='bookmark', lazy='dynamic',
                            cascade='all, delete-orphan',
                            primaryjoin='Bookmark.id==Vote.bookmark_id')
    favourited = db.relationship('Favourite', backref='bookmark',
                                 lazy='dynamic', cascade='all, delete-orphan')

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.id'), nullable=False)

    direction = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        """Representation of a Vote instance."""
        return '<Vote {}>'.format(self.direction)


class Favourite(db.Model):
    """Define what bookmarks each user saved."""

    __tablename__ = 'favourites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.id'), nullable=False)

    saved_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        """Represent a Favourite instance."""
        return '<Favourite {}>'.format(self.saved_on)


class TagSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Tag


class VoteSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Vote

    user = ma.HyperlinkRelated('users_api')
    bookmark = ma.HyperlinkRelated('bookmarks_api.BookmarkAPI', id='<id>')


class FavouriteSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Favourite

    bookmark = ma.HyperlinkRelated('bookmarks_api.BookmarkAPI', id='<id>')
