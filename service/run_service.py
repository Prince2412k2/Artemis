from models.models import Project, Run
from sqlmodel import Session, select
from fastapi import HTTPException
from dependencies import get_random_id
import logging

logger = logging.getLogger(__name__)


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
    return run.identifier


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


def remove_run(run_id: str, session: Session):
    selected_run = session.exec(select(Run).where(Run.identifier == run_id)).first()
    if not selected_run:
        raise HTTPException(status_code=404, detail=f"Run of {run_id=} not found")
    else:
        name = selected_run.name
        session.delete(selected_run)
        session.commit()
        logger.info(f"Run: {name} with ID:{run_id} Removed Sucessfully")
