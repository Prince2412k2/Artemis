from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session
from database import get_db
from crud import register_user,get_users
from pydantic import EmailStr


user_router = APIRouter()

@user_router.post("/register")
def create_user(name: str, email: EmailStr, session: Session = Depends(get_db)):
    try:
        return register_user(
            session=session,
            name=name,
            email=email,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="User Already Exists")

@user_router.get("/get")
def get_all_user(session: Session = Depends(get_db)):
    return get_users(
            session=session,
        )
