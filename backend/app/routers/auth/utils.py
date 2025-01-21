from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.config import settings
from app.utilities.auth_utils import ALGORITHM
from app.utilities.db import db
from app.utilities.redis import redis_client
from app.utilities.static_values import INVALID_TOKEN, TOKEN_EXPIRED, USER_NOT_FOUND

security = HTTPBearer()


def fetch_user_from_db(username: str) -> Any:
    """Fetch user details from MongoDB by username."""
    user = db.users.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )
    return user


def create_access_token(username: str) -> str:
    """Generate a new JWT access token for the given username."""
    expires_at = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(
        {"sub": username, "exp": expires_at},
        settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )


def cache_token_in_redis(username: str, token: str) -> None:
    """Store the access token in Redis with an expiration time."""
    redis_client.setex(
        f"access_token:{username}", settings.access_token_expire_minutes, token
    )


def get_cached_token(username: str) -> str | None:
    """Retrieve the cached access token from Redis if it exists."""
    return redis_client.get(f"access_token:{username}")


def validate_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Validate the access token and return the username.
    """
    token = credentials.credentials
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        username: str = payload["sub"]
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=TOKEN_EXPIRED
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_TOKEN
        )
