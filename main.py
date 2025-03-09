from fastapi import FastAPI
from routes.user import user_router
from routes.workspace import workspace_router
from routes.project import project_router
from routes.run import run_router

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(workspace_router, prefix="/workspace")
app.include_router(project_router, prefix="/project")
app.include_router(run_router, prefix="/run")

app.get("/")


async def home():
    return {"bat": "man"}


# @app.post("/create")
# def create_user(name: str, email: EmailStr, session: Session = Depends(get_db)):
#     try:
#         return register_user(
#             session=session,
#             name=name,
#             email=email,
#         )
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="User Already Exists")
