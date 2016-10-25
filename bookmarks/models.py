"""Create the database schema for the application."""


import arrow

from bookmarks import db, ma


class Category(db.Model):
    """Define column for bookmark categories."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, default='uncategorized')
    bookmarks = db.relationship('Bookmark', backref='category', lazy='dynamic')

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
    image = db.Column(db.String(50), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    votes = db.relationship('Vote', backref='bookmark', lazy='dynamic',
                            primaryjoin='Bookmark.id==Vote.bookmark_id')

    def get_human_time(self):
        """Humanize and return the created_on time."""
        return arrow.get(self.created_on).humanize()

    def __repr__(self):
        """Representation of a Bookmark instance."""
        return '<Bookmark {}>'.format(self.title)


class Vote(db.Model):
    """Define what each user voted for each bookmark."""

    __tablename__ = 'votes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        primary_key=True)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.id'),
                            primary_key=True)

    direction = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        """Representation of a Vote instance."""
        return '<Vote {}>'.format(self.direction)


class Favourite(db.Model):
    """Define what bookmarks each user saved."""

    __tablename__ = 'favourites'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        primary_key=True)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.id'),
                            primary_key=True)

    saved_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        """Representation of a Favourite instance."""
        return '<Favourite {}>'.format(self.saved_on)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


class BookmarkSchema(ma.ModelSchema):
    class Meta:
        model = Bookmark


class VoteSchema(ma.ModelSchema):
    class Meta:
        model = Vote


class FavouriteSchema(ma.ModelSchema):
    class Meta:
        model = Favourite
