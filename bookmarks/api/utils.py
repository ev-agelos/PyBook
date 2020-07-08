from flask import current_app
import requests

def is_recaptcha_valid(token):
    payload = {
        'secret': current_app.config.get('RECAPTCHA_PRIVATE_KEY', ''),
        'response': token
    }
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        payload
    )
    return response.json()['success'] is True
