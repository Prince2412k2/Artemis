from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session
from database import get_db
from crud import create_new_workspace,get_workspace_of_id,get_workspaces
from pydantic import EmailStr


workspace_router = APIRouter()


@workspace_router.post("/create")
def create_workspace(name: str, user_id:int , session: Session = Depends(get_db)):
    try:
        return create_new_workspace(
            session=session,
            name=name,
            user_id=user_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")

@workspace_router.get("/get_all")
def get_all_workspace(session: Session = Depends(get_db)):
    return get_workspaces(
            session=session
        )

@workspace_router.post("/{id}")
def get_workspace_by_id(user_id:str,session: Session = Depends(get_db)):
    try:
        return get_workspace_of_id(
            session=session,
            user_id=user_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="User Doesnt Exist")