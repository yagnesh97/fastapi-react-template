from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from app.config import settings
from app.routers.auth.models import (
    AuthResponse,
    InvalidCredentialsException,
    MeResponse,
    TokenExpiredORInvalidException,
    UserNotFoundException,
)
from app.routers.auth.utils import (
    cache_token_in_redis,
    create_access_token,
    fetch_user_from_db,
    get_cached_token,
    validate_access_token,
)
from app.utilities.auth_utils import verify_password
from app.utilities.redis import redis_client
from app.utilities.static_values import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    INVALID_CREDENTIALS,
)

router = APIRouter()
basic_security = HTTPBasic()
security = HTTPBearer()


@router.get(
    "/login",
    response_model=AuthResponse,
    responses={
        401: {
            "description": HTTP_401_UNAUTHORIZED,
            "model": InvalidCredentialsException,
        }
    },
)
def login(
    response: Response, credentials: HTTPBasicCredentials = Depends(basic_security)
) -> AuthResponse:
    """
    Login to retrieve an access token.
    If a valid non-expired cached token exists, it is returned.
    """
    username = credentials.username
    password = credentials.password

    # Fetch user from the database
    user = fetch_user_from_db(username)

    # Verify password
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS,
        )

    # Check Redis cache for an existing token
    cached_token = get_cached_token(username)
    if cached_token:
        ttl = redis_client.ttl(f"access_token:{username}")
        return AuthResponse(access_token=cached_token, expires_in=ttl)

    # Create and cache a new token
    access_token = create_access_token(username)
    cache_token_in_redis(username, access_token)

    return AuthResponse(
        access_token=access_token, expires_in=settings.access_token_expire_minutes
    )


@router.get(
    "/me",
    response_model=MeResponse,
    responses={
        401: {
            "description": HTTP_401_UNAUTHORIZED,
            "model": TokenExpiredORInvalidException,
        },
        404: {"description": HTTP_404_NOT_FOUND, "model": UserNotFoundException},
    },
)
def me(username: str = Depends(validate_access_token)) -> MeResponse:
    """
    Return the current logged-in user's details.
    """
    # Fetch user details from the database
    user = fetch_user_from_db(username)

    return MeResponse(
        username=user["username"],
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        admin=user["admin"],
    )
