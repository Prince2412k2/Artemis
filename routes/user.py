from typing import Optional
from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session
from database import get_db
from crud import register_user, get_users,remove_user,get_user_of_id
from pydantic import EmailStr
from models.models import TypeUser, UserResponse,Token,UserLogin

from dependencies import create_access_token,verify_password,oauth2_bearer,verify_token
user_router = APIRouter()


@user_router.post("/register",status_code=status.HTTP_201_CREATED)
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

@user_router.post("/login")
def login(user:UserLogin,session:Session= Depends(get_db))->Token:
    real_user =  get_user_of_id(id=user.id,session=session)
    if not verify_password(plain_password=user.password, hashed_password=real_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Generate JWT token
    access_token = create_access_token(data={"sub": real_user.identifier})
    return Token(access_token=access_token,token_type="bearer")


@user_router.get("/get")
def get_all_user(session: Session = Depends(get_db)):
    return get_users(
        session=session,
    )

@user_router.delete("/")
def get_user(session: Session = Depends(get_db),token:str=Depends(oauth2_bearer)):
    payload=verify_token(token=token)
    if payload:
        return remove_user(
            user_id=payload["sub"],
            session=session,
            )
    else :
        raise HTTPException(status_code=404,detail="Invalid JWT token")


