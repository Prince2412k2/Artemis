from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session
from database import get_db
from crud import create_new_run,get_run_of_id,get_runs
from pydantic import EmailStr


run_router = APIRouter()


@run_router.post("/create")
def create_run(name: str, project_id:int , session: Session = Depends(get_db)):
    try:
        return create_new_run(
            session=session,
            name=name,
            project_id=project_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="project already Exists")

@run_router.get("/get_all")
def get_all_runs(session: Session = Depends(get_db)):
    return get_runs(
            session=session
        )

@run_router.post("/{id}")
def get_run_by_id(project_id:str,session: Session = Depends(get_db)):
    try:
        return get_run_of_id(
            session=session,
            project_id=project_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project Doesnt Exist")