from typing import Optional
from models.models import User
from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
from dependencies import verify_password, get_password_hash
import logging
import uuid

logger = logging.getLogger(__name__)


def register_user(
    session: Session,
    name: str,
    email: EmailStr,
    password: Optional[str],
):
    if session.exec(select(User).where(User.name == name)).first():
        raise HTTPException(status_code=404, detail=f"User of {name=} already exists")

    user = User(
        name=name,
        email=email,
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User: {name} added Sucessfully")
    return str(user.id)


def get_users(session: Session):
    return [
        i.model_dump(exclude={"password", "id"}) for i in session.exec(select(User))
    ]


def remove_user(session: Session, user_id: str):
    selected_user = get_user_of_id(user_id, session=session)
    if not selected_user:
        raise HTTPException(status_code=404, detail=f"User of {user_id=} not found")
    else:
        name = selected_user.name
        session.delete(selected_user)
        session.commit()
        logger.info(f"User: {name} with ID:{user_id} Removed Sucessfully")


def get_user_of_id(id_str: str, session: Session):
    id = uuid.UUID(id_str)
    user = session.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User of {id=} not found")
    return user


def get_user_of_name(name: str, session: Session):
    user = session.exec(select(User).where(User.name == name)).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User of name : {name} not found")
    return user


def authenticate_user(user_name: str, password: str, session: Session):
    user = get_user_of_name(name=user_name, session=session)
    if not verify_password(password, user.password):
        return False
    return user
