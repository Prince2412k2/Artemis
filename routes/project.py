from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_sql_db
from service import create_new_project, get_project_of_id, get_projects,remove_project
from pydantic import EmailStr

from models.models import ProjectResponse

from service import oauth2_bearer, verify_token

project_router = APIRouter()


@project_router.post("/create")
def create_project(
    project: ProjectResponse,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    payload = verify_token(token)
    try:
        return create_new_project(
            session=session,
            name=project.name,
            workspace_id=project.workspace_id,
            user_id=payload["sub"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Workspace already Exists")


@project_router.get("/get_all")
def get_all_projects(
    session: Session = Depends(get_sql_db), token: str = Depends(oauth2_bearer)
):
    return get_projects(session=session)


@project_router.post("/{id}")
def get_project_by_id(
    workspace_id: str,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    payload=verify_token(token=token)
    try:
        return get_project_of_id(session=session, workspace_id=workspace_id,user_id=payload["sub"])
    except Exception as e:
        raise HTTPException(status_code=400, detail="Workspace Doesnt Exist")

@project_router.delete("/")
def delete_project(workspace_id:str,
    session: Session = Depends(get_sql_db), token: str = Depends(oauth2_bearer)
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