"""Models for auth package."""


from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.ext.hybrid import hybrid_property

from bookmarks import db, bcrypt
from bookmarks.models import Bookmark, Favourite, Vote


subscriptions = db.Table(
    'subscriptions',
    db.Column('subscriber_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('subscribed_id', db.Integer, db.ForeignKey('users.id'))
)

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
    auth_token = db.Column(db.String(100), default='')
    authenticated = db.Column(db.Boolean, default=False)

    bookmarks = db.relationship(Bookmark, backref='user',
                                cascade='all, delete-orphan', lazy='dynamic')
    favourites = db.relationship(Favourite, backref='user', lazy='dynamic',
                                 cascade='all, delete-orphan')
    votes = db.relationship(Vote, backref='user', lazy='dynamic',
                            cascade='all, delete-orphan')
    subscribed = db.relationship(
        'User', secondary=subscriptions,
        primaryjoin=(subscriptions.c.subscriber_id == id),
        secondaryjoin=(subscriptions.c.subscribed_id == id),
        backref=db.backref('subscribers', lazy='dynamic'), lazy='dynamic')

    @hybrid_property
    def password(self):
        """Password getter."""
        return self._password

    @password.setter
    def password(self, plaintext):
        """Hash password before setting it."""
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_password_correct(self, plaintext):
        """Check if user's password is correct."""
        return bcrypt.check_password_hash(self._password, plaintext)

    def generate_auth_token(self, expires_in=3600, **kwargs):
        """Return a new token for the user."""
        serializer = Serializer(current_app.config['SECRET_KEY'],
                                expires_in=expires_in)
        kwargs.update(id=self.id)
        return serializer.dumps(kwargs).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        """Verify token for a user."""
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except:
            return {}
        return data

    def subscribe(self, user):
        if not self.is_subscribed_to(user):
            self.subscribed.append(user)
            return self
        return None

    def unsubscribe(self, user):
        if self.is_subscribed_to(user):
            self.subscribed.remove(user)
            return self
        return None

    def is_subscribed_to(self, user):
        return self.subscribed.filter(
            subscriptions.c.subscribed_id == user.id).count() > 0

    def __repr__(self):
        """Representation of a User instance."""
        return '<User {}>'.format(self.username)
