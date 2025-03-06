from fastapi import FastAPI, HTTPException, status
from fastapi import APIRouter, Depends
from sqlalchemy import Exists
from sqlmodel import Session
from database import get_db
from crud import register_user
from pydantic import EmailStr

app = FastAPI()


@app.post("/create")
def create_user(name: str, email: EmailStr, session: Session = Depends(get_db)):
    try:
        return register_user(
            session=session,
            name=name,
            email=email,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="User Already Exists")
