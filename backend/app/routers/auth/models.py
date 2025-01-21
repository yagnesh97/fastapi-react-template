from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints

from app.utilities.static_values import (
    INVALID_CREDENTIALS,
    INVALID_TOKEN,
    TOKEN_EXPIRED,
    USER_NOT_FOUND,
)

UsernameStr = Annotated[
    str,
    StringConstraints(min_length=3, max_length=15, pattern=r"^[a-z0-9_-]{3,15}$"),
]


class AuthResponse(BaseModel):
    access_token: Optional[str] = None
    expires_in: Optional[int] = None


class MeResponse(BaseModel):
    username: UsernameStr
    email: EmailStr
    first_name: str
    last_name: str
    admin: bool


class InvalidCredentialsException(BaseModel):
    detail: str = INVALID_CREDENTIALS


class TokenExpiredORInvalidException(BaseModel):
    detail: str = f"{TOKEN_EXPIRED} / {INVALID_TOKEN}"


class UserNotFoundException(BaseModel):
    detail: str = USER_NOT_FOUND
