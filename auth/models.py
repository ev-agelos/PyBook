"""Models for auth package."""


from sqlalchemy.ext.hybrid import hybrid_property

from main import db, bcrypt


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
    username = db.Column(db.String(30))
    email = db.Column(db.String(30))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=db.func.now())
    _password = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)
    email_token = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    bookmarks = db.relationship('Bookmark', backref='user',
                                cascade='all, delete-orphan', lazy='dynamic')

    @hybrid_property
    def password(self):
        """Getter for password."""
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        """Setter for password."""
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_password_correct(self, plaintext):
        """Check if user's password is correct."""
        return bcrypt.check_password_hash(self._password, plaintext)

    def is_active(self):
        """Return if user is active or not."""
        return self.active

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
