import uuid
from typing import List
from models.models import Workspace, Project
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import logging

from service.user_service import get_user_of_id


logger = logging.getLogger(__name__)


def create_new_project(session: Session, name: str, workspace_id: str, user_id: str):
    
    user = get_user_of_id(id_str=user_id, session=session)
    workspace=session.exec(
        select(Workspace).where(Workspace.id == uuid.UUID(workspace_id))).first()
    
    if not workspace:
        raise HTTPException(
            status_code=404, detail=f"workspace of {workspace_id=} not found"
        )
    
    projects=session.exec(select(Project).where(Project.name==name)).all()
    if [i for i in projects if i.workspace_id==uuid.UUID(workspace_id)]:
        raise HTTPException(status_code=404,detail=f"Project of name : {name} already exists")
    
    
    project = Project(
            name=name,
            workspace_id=uuid.UUID(workspace_id),
            user_id=uuid.UUID(user_id),
        )
    try:

        session.add(project)
        session.commit()
        session.refresh(project)
        return project.id
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Project name must be unique for the Workspace")


def get_project_of_workspace(session: Session, workspace_id: str):
    if not session.exec(
        select(Workspace).where(Workspace.id == uuid.UUID(workspace_id))
    ).first():
        raise HTTPException(
            status_code=404, detail=f"workspace of {workspace_id=} not found"
        )
    projects = session.exec(
        select(Project).where(Project.workspace_id == uuid.UUID(workspace_id))
    ).all()
    if not projects:
        raise HTTPException(
            status_code=404, detail="No projects found for this workspace."
        )
    return [i.model_dump() for i in projects]


def get_projects_of_user(session: Session, user_id: str) -> List[Project]:
    projects_of_user = list(
        session.exec(select(Project).where(Project.user_id == uuid.UUID(user_id))).all()
    )
    return projects_of_user


def get_projects(session: Session):
    return [i.model_dump() for i in session.exec(select(Project))]


def remove_project(user_id: str, project_id: str, session: Session):
    selected_project = session.exec(
        select(Project).where(Project.id == uuid.UUID(project_id))
    ).first()
    if not selected_project:
        raise HTTPException(
            status_code=404, detail=f"Project of {project_id=} not found"
        )
    else:
        name = selected_project.name
        session.delete(selected_project)
        session.commit()
        logger.info(f"Project: {name} with ID:{project_id} Removed Sucessfully")
