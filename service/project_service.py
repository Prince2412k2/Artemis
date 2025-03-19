from typing import Optional
from models.models import User, Workspace, Project, Run, TypeUser, Token
from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
from dependencies import get_random_id, verify_password, get_password_hash
import logging


logger = logging.getLogger(__name__)


def create_new_project(session: Session, name: str, workspace_id: str, user_id: str):
    if not session.exec(
        select(Workspace).where(Workspace.identifier == workspace_id)
    ).first():
        raise HTTPException(
            status_code=404, detail=f"workspace of {workspace_id=} not found"
        )
    all_identifiers = list(session.exec(select(Project.identifier)).all())
    project = Project(
        name=name,
        workspace_id=workspace_id,
        identifier=get_random_id(all_identifiers),
        user_id=user_id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project.identifier


def get_project_of_id(session: Session, workspace_id: str):
    if not session.exec(
        select(Workspace).where(Workspace.identifier == workspace_id)
    ).first():
        raise HTTPException(
            status_code=404, detail=f"workspace of {workspace_id=} not found"
        )
    projects = session.exec(
        select(Project).where(Project.workspace_id == workspace_id)
    ).all()
    if not projects:
        raise HTTPException(
            status_code=404, detail="No projects found for this workspace."
        )
    return [i.model_dump(exclude={"id"}) for i in projects]


def get_projects(session: Session):
    return [i.model_dump(exclude={"id"}) for i in session.exec(select(Project))]


def remove_project(user_id:str,project_id: str, session: Session):
    selected_project = session.exec(
        select(Project).where(Project.identifier == project_id)
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
