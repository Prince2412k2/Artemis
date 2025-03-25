import stat
from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException
import logging
import uuid
from sqlalchemy.exc import IntegrityError

from models.models import Project, Run
from service.user_service import get_user_of_id

logger = logging.getLogger(__name__)


def create_new_run(session: Session, name: str, project_id: str, user_id: str):
    project= session.exec(
        select(Project).where(Project.id == uuid.UUID(project_id))
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=404, detail=f"Project of {project_id=} not found"
        )
    runs=session.exec(select(Run).where(Run.name==name)).all()
    
    runs_in_project=[i for i in runs if i.project_id == uuid.UUID(project_id)]
    if runs_in_project:
        raise HTTPException(status_code=404,detail=f"Run with name : {name} already exists")
    
    
    run = Run(
        name=name,
        project_id=uuid.UUID(project_id),
        user_id=uuid.UUID(user_id),
    )
    
    try:

        session.add(run)
        session.commit()
        session.refresh(run)
        return run.id
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Run name must be unique for the Project")
    



def get_runs_of_user(session: Session, user_id: str) -> List[Run]:
    runs_of_user = list(session.exec(select(Run).where(Run.user_id == uuid.UUID(user_id))).all())
    return runs_of_user


def get_run_of_project(session: Session, project_id: str) -> List[Run]:
    if not session.exec(select(Project).where(Project.id == uuid.UUID(project_id))).first():
        raise HTTPException(
            status_code=404, detail=f"Project of {project_id=} not found"
        )
    runs = list(session.exec(select(Run).where(Run.project_id == uuid.UUID(project_id))).all())
    if runs:
        return runs
    raise HTTPException(status_code=404, detail="No runs found for this project.")


def get_runs(session: Session):
    return [i.model_dump(exclude={"id"}) for i in session.exec(select(Run))]


def remove_run(run_id: str, session: Session):
    selected_run = session.exec(select(Run).where(Run.id == uuid.UUID(run_id))).first()
    if not selected_run:
        raise HTTPException(status_code=404, detail=f"Run of {run_id=} not found")
    else:
        name = selected_run.name
        session.delete(selected_run)
        session.commit()
        logger.info(f"Run: {name} with ID:{run_id} Removed Sucessfully")
