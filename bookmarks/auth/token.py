"""Helper functions for handling tokens."""

from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer


def generate_user_token(email):
    """Generate token with the email address."""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email)


def confirm_token(token, expiration=3600):
    """Confirm a given token if it is valid."""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, max_age=expiration)
    except Exception:
        return False
    return email
