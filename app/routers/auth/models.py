from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class User(UserBase):
    admin: bool = False
    active: bool = False


class Register(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    admin: Optional[bool] = None
    active: Optional[bool] = None


class UserInDB(User):
    hashed_password: bytes
