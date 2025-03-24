from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_sql_db

from service import (
    create_new_run,
    get_run_of_project,
    get_runs_of_user,
    get_runs,
    remove_run,
)
from models.models import RunResponse, Run
from dependencies import oauth2_bearer, verify_token

run_router = APIRouter()


@run_router.post("/create")
def create_run(
    run: RunResponse,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    payload = verify_token(token=token)
    if payload:
        try:
            return create_new_run(
                session=session,
                name=run.name,
                project_id=str(run.project_id),
                user_id=payload["sub"],
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"[create_run] threw a Exception : {e}"
            )


@run_router.get("/get_all")
def get_all_runs(
    session: Session = Depends(get_sql_db), token: str = Depends(oauth2_bearer)
):
    return get_runs(session=session)


@run_router.get("/my")
def get_run_by_user(
    session: Session = Depends(get_sql_db), token: str = Depends(oauth2_bearer)
) -> Optional[List[Run]]:
    payload = verify_token(token=token)
    if payload:
        return get_runs_of_user(session=session, user_id=payload["sub"])


@run_router.post("/{project_id}")
def get_run_by_project_id(
    project_id: str,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    if verify_token(token):
        try:
            return get_run_of_project(session=session, project_id=project_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Project Doesnt Exist")


@run_router.delete("/")
def delete_run(
    run_id: str,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    if verify_token(token=token):
        return remove_run(
            run_id=run_id,
            session=session,
        )
    else:
        raise HTTPException(status_code=404, detail="Invalid JWT token")
