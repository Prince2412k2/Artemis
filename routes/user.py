from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_db
from crud import register_user, get_users,remove_user
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

@user_router.delete("/{id}")
def get_all_user(user_id:str,session: Session = Depends(get_db)):
    return remove_user(
        user_id=user_id,
        session=session,
    )


