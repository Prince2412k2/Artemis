from typing import Optional
from models.models import User, Workspace, Project, Run, TypeUser, Token
from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
import logging

from service.user_service import get_user_of_id

from dependencies import get_random_id, verify_password, get_password_hash

logger = logging.getLogger(__name__)


def create_new_workspace(session: Session, name: str, user_id: str):
    get_user_of_id(id=user_id, session=session)
    all_identifiers = list(session.exec(select(Workspace.identifier)).all())
    workspace = Workspace(
        name=name, user_id=user_id, identifier=get_random_id(all_identifiers)
    )
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    logger.info(f"Workspace :{name} added Sucessfully")
    return workspace.identifier


def get_workspace_of_id(session: Session, user_id: str):
    if not session.exec(select(User).where(User.identifier == user_id)).first():
        raise HTTPException(status_code=404, detail=f"User of {user_id=} not found")

    workspaces = session.exec(
        select(Workspace).where(Workspace.user_id == user_id)
    ).all()
    if not workspaces:
        raise HTTPException(
            status_code=404, detail="No workspaces found for this user."
        )
    return [i.model_dump(exclude={"id"}) for i in workspaces]


def get_workspaces(session: Session):
    return [i.model_dump(exclude={"id"}) for i in session.exec(select(Workspace))]


def remove_workspace(workspace_id: str, session: Session):
    selected_workspace = session.exec(
        select(Workspace).where(Workspace.identifier == workspace_id)
    ).first()
    if not selected_workspace:
        raise HTTPException(
            status_code=404, detail=f"Workspace of {workspace_id=} not found"
        )
    else:
        name = selected_workspace.name
        session.delete(selected_workspace)
        session.commit()
        logger.info(f"Workspace: {name} with ID:{workspace_id} Removed Sucessfully")
