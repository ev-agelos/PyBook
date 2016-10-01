"""Helper functions for handling tokens."""

from itsdangerous import URLSafeTimedSerializer


def generate(email, secret_key):
    """Generate token with the email address."""
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email)


def confirm(token, secret_key, expiration=3600):
    """Confirm a given token if it is valid."""
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(token, max_age=expiration)
    except Exception:
        return False
    return email
