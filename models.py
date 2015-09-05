"""Create the database schema for the application."""


from app import db


class User(db.Model):

    """Define columns for User table."""

    __tablename__ = 'users'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Bookmark(db.Model):

    """"Define columns for bookmarks table."""

    __tablename__ = 'bookmarks'

    bookmark_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True, unique=True)

    def __init__(self, category, title, url):
        """Set the values when an instance is initialised."""
        self.category = category
        self.title = title
        self.url = url

    def __repr__(self):
        """Representation of a Bookmark instance."""
        return self.title
