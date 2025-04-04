from models.models import User, Workspace
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import logging
import uuid
from service.user_service import get_user_of_id

logger = logging.getLogger(__name__)


def create_new_workspace(session: Session, name: str, user_id: str):
    get_user_of_id(id_str=user_id, session=session)
    workspace=session.exec(select(Workspace).where(Workspace.name==name)).all()
        
    workspaces_in_project=[i for i in workspace if i.user_id == uuid.UUID(user_id)]
    if workspaces_in_project:
        raise HTTPException(status_code=404,detail=f"Workspcae of name : {name} already exists")
    
    workspace = Workspace(name=name, user_id=uuid.UUID(user_id))
    try:
        session.add(workspace)
        session.commit()
        session.refresh(workspace)
        return workspace
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Workspace name must be unique for the user")



def get_workspace_of_id(session: Session, user_id: str):
    workspaces = session.exec(
        select(Workspace).where(Workspace.user_id == uuid.UUID(user_id))
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
