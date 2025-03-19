from typing import Optional
from models.models import User, Workspace, Project, Run, TypeUser, Token
from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
from dependencies import get_random_id, verify_password, get_password_hash
import logging

logger = logging.getLogger(__name__)


def register_user(
    session: Session,
    name: str,
    email: EmailStr,
    password: Optional[str],
    user_type: TypeUser,
):
    if user_type == TypeUser.PROTECTED and not password:
        raise (
            HTTPException(
                status_code=400, detail="Protected acoounts require valid password"
            )
        )
    if session.exec(select(User).where(User.name == name)).first():
        raise HTTPException(status_code=404, detail=f"User of {name=} already exists")
    all_identifiers = list(session.exec(select(User.identifier)).all())
    user = User(
        name=name,
        email=email,
        password=get_password_hash(password),
        user_type=user_type,
        identifier=get_random_id(all_identifiers),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User: {name} added Sucessfully")
    return user.identifier


def get_users(session: Session):
    return [
        i.model_dump(exclude={"password", "id"}) for i in session.exec(select(User))
    ]


def remove_user(session: Session, user_id: str):
    selected_user = session.exec(select(User).where(User.identifier == user_id)).first()
    if not selected_user:
        raise HTTPException(status_code=404, detail=f"User of {user_id=} not found")
    else:
        name = selected_user.name
        session.delete(selected_user)
        session.commit()
        logger.info(f"User: {name} with ID:{user_id} Removed Sucessfully")


def get_user_of_id(id: str, session: Session):
    user = session.exec(select(User).where(User.identifier == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User of {id=} not found")
    return user


def authenticate_user(user_id: str, password: str, session: Session):
    user = get_user_of_id(id=user_id, session=session)
    if not verify_password(password, user.password):
        return False
    return user
