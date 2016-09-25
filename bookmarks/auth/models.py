"""Models for auth package."""


from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from bookmarks import db, bcrypt
from bookmarks.models import Bookmark


class User(db.Model, UserMixin):
    """
    Define columns for User table.

    backref: adds attribute to Bookmark instance to use it like: bookmark.user
    cascade: delete all bookmarks related to User when User is deleted
    lazy: return a query object which you can refine further like if you want
        to add a limit etc
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(30))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    _password = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)
    email_token = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    bookmarks = db.relationship(Bookmark, backref='user',
                                cascade='all, delete-orphan', lazy='dynamic')

    @hybrid_property
    def password(self):
        """Password getter."""
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        """Hash password before setting it."""
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_password_correct(self, plaintext):
        """Check if user's password is correct."""
        return bcrypt.check_password_hash(self._password, plaintext)

    def __repr__(self):
        """Representation of a User instance."""
        return '<User {}>'.format(self.username)
