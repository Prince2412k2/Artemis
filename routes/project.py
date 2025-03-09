from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_db
from crud import create_new_project, get_project_of_id, get_projects
from pydantic import EmailStr

from models.models import ProjectResponse


project_router = APIRouter()


@project_router.post("/create")
def create_project(project: ProjectResponse, session: Session = Depends(get_db)):
    try:
        return create_new_project(
            session=session,
            name=project.name,
            workspace_id=project.workspace_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Workspace already Exists")


@project_router.get("/get_all")
def get_all_projects(session: Session = Depends(get_db)):
    return get_projects(session=session)


@project_router.post("/{id}")
def get_project_by_id(workspace_id: str, session: Session = Depends(get_db)):
    try:
        return get_project_of_id(session=session, workspace_id=workspace_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Workspace Doesnt Exist")
