from typing import Optional
from models.models import User, Workspace, Project, Run, TypeUser
from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
from dependencies import get_random_id


# ---- User ----
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
    all_identifiers = list(session.exec(select(User.identifier)).all())
    user = User(
        name=name,
        email=email,
        password=password,
        user_type=user_type,
        identifier=get_random_id(all_identifiers),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_users(session: Session):
    return [
        i.model_dump(exclude={"password", "id"}) for i in session.exec(select(User))
    ]


# ---- Workspace ----


def create_new_workspace(session: Session, name: str, user_id: str):
    if not session.exec(select(User).where(User.identifier == user_id)).first():
        raise HTTPException(status_code=404, detail=f"User of {user_id=} not found")
    all_identifiers = list(session.exec(select(Workspace.identifier)).all())
    workspace = Workspace(
        name=name, user_id=user_id, identifier=get_random_id(all_identifiers)
    )
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    return workspace


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


# ---- Project ----
def create_new_project(session: Session, name: str, workspace_id: str):
    if not session.exec(
        select(Workspace).where(Workspace.identifier == workspace_id)
    ).first():
        raise HTTPException(
            status_code=404, detail=f"workspace of {workspace_id=} not found"
        )

    all_identifiers = list(session.exec(select(Project.identifier)).all())
    project = Project(
        name=name, workspace_id=workspace_id, identifier=get_random_id(all_identifiers)
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


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


# ---- Run ----
def create_new_run(session: Session, name: str, project_id: str):
    if not session.exec(
        select(Project).where(Project.identifier == project_id)
    ).first():
        raise HTTPException(
            status_code=404, detail=f"Project of {project_id=} not found"
        )
    all_identifiers = list(session.exec(select(Run.identifier)).all())
    run = Run(
        name=name, project_id=project_id, identifier=get_random_id(all_identifiers)
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def get_run_of_id(session: Session, project_id: str):
    if not session.exec(
        select(Project).where(Project.identifier == project_id)
    ).first():
        raise HTTPException(
            status_code=404, detail=f"Project of {project_id=} not found"
        )
    runs = session.exec(select(Run).where(Run.project_id == project_id)).all()
    if not runs:
        raise HTTPException(status_code=404, detail="No runs found for this project.")
    return [i.model_dump(exclude={"id"}) for i in runs]


def get_runs(session: Session):
    return [i.model_dump(exclude={"id"}) for i in session.exec(select(Run))]
