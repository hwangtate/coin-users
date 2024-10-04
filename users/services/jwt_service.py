from datetime import datetime, timedelta

import jwt

from config import settings


def generate_access_token(user_id):
    access_token_payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(minutes=1),
        "iat": datetime.now(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256")
    return access_token


def generate_refresh_token(user_id):
    refresh_token_payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(days=7),
        "iat": datetime.now(),
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256")
    return refresh_token
