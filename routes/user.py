from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_db
from crud import register_user, get_users
from pydantic import EmailStr
from models.models import TypeUser, UserResponse

user_router = APIRouter()


@user_router.post("/register")
def create_user(
    user: UserResponse,
    session: Session = Depends(get_db),
):
    return register_user(
        session=session,
        name=user.name,
        email=user.email,
        password=user.password,
        user_type=user.user_type,
    )


@user_router.get("/get")
def get_all_user(session: Session = Depends(get_db)):
    return get_users(
        session=session,
    )
