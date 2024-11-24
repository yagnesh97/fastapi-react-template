from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .models import Register, Token, User, UserUpdate
from .utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    is_admin_user,
    register_user,
    update_user,
)

router = APIRouter()


@router.post("/token", summary="Fetch authentication token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User, summary="Register a user")
async def register(payload: Register):
    user = register_user(data=payload)
    return user


@router.get("/users/me", response_model=User, summary="Fetch logged-in user's details")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.put("/users/{username}", response_model=User, summary="Update a user")
async def update_users(
    username: str,
    payload: UserUpdate,
    current_user: Annotated[User, Depends(is_admin_user)],
):
    user = update_user(username=username, data=payload, current_user=current_user)
    return user
