from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_db
from crud import register_user
from pydantic import EmailStr

router = APIRouter()


@router.route("/create")
def create_user(name: str, email: EmailStr, session: Session = Depends(get_db)):
    return register_user(
        session=session,
        name=name,
        email=email,
    )
