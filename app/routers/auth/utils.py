from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.config import settings
from app.utilities.db import db

from .models import Register, TokenData, User, UserInDB, UserUpdate

# Constants
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """Verifies if the provided password matches the hashed password."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password)


def get_password_hash(password: str) -> bytes:
    """Hashes the password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def get_user(username: str) -> Optional[UserInDB]:
    """Fetches the user from the database by username if active."""
    record = db.users.find_one({"username": username, "active": True})
    return UserInDB(**record) if record else None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticates the user by verifying the username and password."""
    user = get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """Retrieves the current user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Checks if the current user is active."""
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def is_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Checks if the current user is an admin."""
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges to perform this action.",
        )
    return current_user


def register_user(
    data: Register,
) -> User:
    """Registers a new user without active false."""
    record = db.users.find_one(
        {"$or": [{"username": data.username}, {"email": data.email}]},
        {"username": 1, "email": 1},
    )
    if not record:
        now = datetime.now(tz=timezone.utc)
        hashed_password = get_password_hash(data.password)
        insert_data = UserInDB(
            **data.model_dump(), hashed_password=hashed_password
        ).model_dump()
        insert_data.update(
            {
                "created_by": data.username,
                "created_date": now,
                "updated_by": data.username,
                "updated_date": now,
            }
        )
        result = db.users.insert_one(insert_data)
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong.",
            )
        return User(**insert_data)

    field = "Username" if record["username"] == data.username else "Email"
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field} already exists."
    )


def update_user(username: str, data: UserUpdate, current_user: User) -> User:
    """Updates a user."""
    query = {"username": username}
    record = db.users.find_one(query)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found."
        )

    now = datetime.now(tz=timezone.utc)
    update_data = {
        **record,
        **data.model_dump(exclude_none=True, exclude_unset=True),
        "updated_by": current_user.username,
        "updated_date": now,
    }
    result = db.users.update_one(query, {"$set": update_data})
    if not result.modified_count:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="Something went wrong.",
        )
    return User(**update_data)
