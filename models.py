"""Create the database schema for the application."""


from app import db


class User(db.Model):

    """
    Define columns for User table.

    backref: adds attribute to Bookmark instance to use it like: bookmark.user
    cascade: delete all bookmarks related to User when User is deleted
    lazy: return a query object which you can refine further like if you want
        to add a limit etc
    """

    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    authenticated = db.Column(db.Boolean, default=False)
    bookmarks = db.relationship('Bookmark', backref='user',
                                cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, username, email, password):
        """Create new user."""
        self.username = username
        self.email = email
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return a unique identifier for a user instance."""
        return self._id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        """Representation of a User instance."""
        return '<User {}>'.format(self.username)


class Bookmark(db.Model):

    """"Define columns for bookmarks table."""

    __tablename__ = 'bookmarks'

    _id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), nullable=True)
    title = db.Column(db.String(50))
    url = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'))

    def __init__(self, category, title, url, user_id):
        """Set the values when an instance is initialised."""
        self.category = category
        self.title = title
        self.url = url
        self.user_id = user_id

    def __repr__(self):
        """Representation of a Bookmark instance."""
        return '<Bookmark {}>'.format(self.title)
