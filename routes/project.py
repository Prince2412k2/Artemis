import logging
from typing import Optional, Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_sql_db
from service import (
    create_new_project,
    get_project_of_workspace,
    get_projects_of_user,
    get_projects,
    remove_project,
)

from models.models import Project, ProjectResponse

from service import oauth2_bearer, verify_token

logger = logging.getLogger(__name__)
project_router = APIRouter()


@project_router.post("/create")
async def create_project(
    project: ProjectResponse,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    payload = verify_token(token)
    if payload:
        return create_new_project(
                session=session,
                name=project.name,
                workspace_id=str(project.workspace_id),
                user_id=payload["sub"],
            )


@project_router.get("/get_all")
async def get_all_projects(session: Session = Depends(get_sql_db)):
    return get_projects(session=session)


@project_router.post("/{workspace_id}")
async def get_project_by_workspace_id(
    workspace_id: str,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
) -> Optional[List[Dict[str, Any]]]:
    if verify_token(token=token):
        try:
            return get_project_of_workspace(session=session, workspace_id=workspace_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    else:
        return [{}]


@project_router.get("/my")
async def get_project_by_user(
    session: Session = Depends(get_sql_db), token: str = Depends(oauth2_bearer)
) -> Optional[List[Project]]:
    payload = verify_token(token=token)
    if payload:
        return get_projects_of_user(session=session, user_id=payload["sub"])


@project_router.delete("/")
async def delete_project(
    workspace_id: str,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    payload = verify_token(token=token)
    if payload:
        return remove_project(
            user_id=payload["sub"],
            project_id=workspace_id,
            session=session,
        )
    else:
        raise HTTPException(status_code=404, detail="Invalid JWT token")
