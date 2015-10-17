"""The secret sauce to solve circual dependencies issues."""

from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension

from bookmarks import app, db
from bookmarks.views import bookmarks, bookmarks_crud, auth, users
from bookmarks.models import User


login_manager = LoginManager()
login_manager.init_app(app)

csrf = CsrfProtect()
csrf.init_app(app)

toolbar = DebugToolbarExtension()
toolbar.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    """Reload the user object from the user ID stored in the session."""
    return db.session.query(User).get(user_id)


if __name__ == '__main__':
    app.run()
