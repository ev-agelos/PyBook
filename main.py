"""The secret sauce to solve circual dependencies issues."""

from app import app
from views import views, auth
from models import User
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CsrfProtect()
csrf.init_app(app)

app.register_blueprint(auth.login_Bp)
app.register_blueprint(auth.logout_Bp)


@login_manager.user_loader
def user_loader(user_id):
    """Reload the user object from the user ID stored in the session."""
    return User.query.get(user_id)


if __name__ == '__main__':
    app.run()
