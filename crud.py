from models.models import User, Workspace, Project, Run
from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
from dependencies import get_random_id


# ---- User ----
def register_user(session: Session, name: str, email: EmailStr):
    all_identifiers = session.exec(select(User.identifier)).all()
    user = User(name=name, email=email, identifier=get_random_id(all_identifiers))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_users(session: Session):
    return session.exec(select(User)).all()


# ---- Workspace ----

def create_new_workspace(session: Session, name: str, user_id: int):
    all_identifiers = session.exec(select(Workspace.identifier)).all()
    workspace = Workspace(
        name=name, user_id=user_id, identifier=get_random_id(all_identifiers)
    )
    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    return workspace


def get_workspace_of_id(session: Session, user_id: int):
    workspaces = session.exec(
        select(Workspace).where(Workspace.user_id == user_id)
    ).all()
    if not workspaces:
        raise HTTPException(
            status_code=404, detail="No workspaces found for this user."
        )
    return workspaces

def get_workspaces(session: Session):
    return session.exec(select(Workspace)).all()


# ---- Project ----
def create_new_project(session: Session, name: str, workspace_id: int):
    all_identifiers = session.exec(select(Project.identifier)).all()
    project = Project(
        name=name, workspace_id=workspace_id, identifier=get_random_id(all_identifiers)
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def get_project_of_id(session: Session, workspace_id: int):
    projects = session.exec(
        select(Project).where(Project.workspace_id == workspace_id)
    ).all()
    if not projects:
        raise HTTPException(
            status_code=404, detail="No projects found for this workspace."
        )
    return projects

def get_projects(session: Session):
    return session.exec(select(Project)).all()


# ---- Run ----
def create_new_run(session: Session, name: str, project_id: int):
    all_identifiers = session.exec(select(Run.identifier)).all()
    run = Run(
        name=name, project_id=project_id, identifier=get_random_id(all_identifiers)
    )
    session.add(run)
    session.commit()
    session.refresh(run)
    return run


def get_run_of_id(session: Session, project_id: int):
    runs = session.exec(select(Run).where(Run.project_id == project_id)).all()
    if not runs:
        raise HTTPException(status_code=404, detail="No runs found for this project.")
    return runs

def get_runs(session: Session):
    return session.exec(select(Run)).all()
