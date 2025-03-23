from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_sql_db
from service import (
    create_new_workspace,
    get_workspace_of_id,
    get_workspaces,
    remove_workspace,
)
from models.models import WorkspaceResponse
from service import (
    oauth2_bearer,
    verify_token,
)

workspace_router = APIRouter()


@workspace_router.post("/create")
def create_workspace(
    workspace: WorkspaceResponse,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    payload = verify_token(token=token)
    if payload:
        try:
            return create_new_workspace(
                session=session,
                name=workspace.name,
                user_id=payload["sub"],
            )
        except Exception as e:
            raise Exception({e})
    else:
        raise HTTPException(status_code=404, detail="Invalid JWT token")


@workspace_router.get("/get_all")
def get_all_workspace(session: Session = Depends(get_sql_db)):
    return get_workspaces(session=session)


@workspace_router.post("/my")
def get_workspace_by_user_id(
    session: Session = Depends(get_sql_db), token: str = Depends(oauth2_bearer)
):
    payload = verify_token(token=token)
    if payload:
        return get_workspace_of_id(session=session, user_id=payload["sub"])
    else:
        raise HTTPException(status_code=404, detail="Invalid JWT token")


@workspace_router.delete("/")
def delete_workspace(
    workspace_id: str,
    session: Session = Depends(get_sql_db),
    token: str = Depends(oauth2_bearer),
):
    payload = verify_token(token=token)
    if payload:
        return remove_workspace(
            workspace_id=workspace_id,
            session=session,
        )
    else:
        raise HTTPException(status_code=404, detail="Invalid JWT token")
