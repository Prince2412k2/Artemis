import logging
from fastapi import FastAPI
from routes.user import user_router
from routes.workspace import workspace_router
from routes.project import project_router
from routes.run import run_router
from dependencies import configure_logger
import uvicorn

app = FastAPI()
logger = configure_logger(log_level=logging.WARNING)


app.include_router(user_router, prefix="/user")
app.include_router(workspace_router, prefix="/workspace")
app.include_router(project_router, prefix="/project")
app.include_router(run_router, prefix="/run")


@app.get("/")
async def home():
    return {"Welcome": "User"}


if __name__ == "__main__":
    uvicorn.run("main:app", log_level="trace")
