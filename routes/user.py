from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from database import get_sql_db
from service import register_user, get_users, remove_user, get_user_of_id
from models.models import UserRequest, Token, UserLogin
from service import (
    authenticate_user,
    create_access_token,
    oauth2_bearer,
    verify_token,
)

user_router = APIRouter()


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserRequest,
    session: Session = Depends(get_sql_db),
):
    return register_user(
        session=session,
        name=user.name,
        email=user.email,
        password=user.password,
    )


@user_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_sql_db),
) -> Optional[Token]:
    user_db = authenticate_user(form_data.username, form_data.password, session=session)
    if user_db:
        access_token = create_access_token(data={"sub": str(user_db.id)})
        return Token(access_token=access_token, token_type="bearer")


@user_router.get("/get_all")
async def get_all_user(session: Session = Depends(get_sql_db)):
    return get_users(
        session=session,
    )


@user_router.delete("/")
async def delete_user(
    session: Session = Depends(get_sql_db), token: str = Depends(oauth2_bearer)
):
    payload = verify_token(token=token)
    if payload:
        return remove_user(
            user_id=payload["sub"],
            session=session,
        )
