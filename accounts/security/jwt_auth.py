import os
import jwt

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from ..models import User


def create_access_token(user_id, role):
    payload: dict = {
        "user_id": user_id,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=1)
    }

    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise Exception("JWT_SECRET_KEY not found in .env")

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_access_token(token):
    try:
        secret_key = os.getenv("JWT_SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["user_id"]

    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed("Access token has expired") from e

    except jwt.InvalidTokenError as e:
        raise AuthenticationFailed("Invalid access token") from e



def create_refresh_token(user_id, role):
    payload: dict = {
        "user_id": user_id,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }

    secret_key = os.getenv("JWT_REFRESH_SECRET_KEY")
    if not secret_key:
        raise Exception("JWT_REFRESH_SECRET_KEY not found in .env")

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_refresh_token(token):
    try:
        secret_key = os.getenv("JWT_REFRESH_SECRET_KEY")
        payload = jwt.decode(token,secret_key,algorithms=["HS256"])

        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Refresh token has expired")

    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid refresh token")



