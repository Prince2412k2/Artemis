from models.models import User, Workspace
from sqlmodel import Session, select
from fastapi import HTTPException
import logging
import uuid
from service.user_service import get_user_of_id

logger = logging.getLogger(__name__)


def create_new_workspace(session: Session, name: str, user_id: str):
    get_user_of_id(id_str=user_id, session=session)
    if session.exec(select(Workspace).where(Workspace.name==name)).first():
        raise HTTPException(status_code=404,detail=f"Workspcae of name : {name} already exists")
    workspace = Workspace(name=name, user_id=user_id)
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    logger.info(f"Workspace :{name} added Sucessfully")
    return workspace.id


def get_workspace_of_id(session: Session, user_id: str):
    workspaces = session.exec(
        select(Workspace).where(Workspace.user_id == user_id)
    ).all()
    if not workspaces:
        raise HTTPException(
            status_code=404, detail="No workspaces found for this user."
        )
    return [i.model_dump() for i in workspaces]


def get_workspaces(session: Session):
    return [i.model_dump() for i in session.exec(select(Workspace))]


def remove_workspace(workspace_id: str, session: Session):
    selected_workspace = session.exec(
        select(Workspace).where(Workspace.id == uuid.UUID(workspace_id))
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
