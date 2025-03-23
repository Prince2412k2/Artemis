from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from database import engine
import uuid

##Enums
# class TypeUser(Enum):
#    PUBLIC = "PUBLIC"
#    PROTECTED = "PROTECTED"


##AUth
class Token(BaseModel):
    access_token: str
    token_type: str


##User
class UserRequest(SQLModel):
    name: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True)
    password: Optional[str] = None


class User(UserRequest, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    workspaces: List["Workspace"] = Relationship(back_populates="user")


class UserLogin(BaseModel):
    name: str
    password: str


# Workspace
class WorkspaceResponse(SQLModel):
    name: str


class Workspace(WorkspaceResponse, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="workspaces")
    projects: List["Project"] = Relationship(back_populates="workspace")


##Project
class ProjectResponse(SQLModel):
    name: str
    workspace_id: str = Field(foreign_key="workspace.id")


class Project(ProjectResponse, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    workspace: Optional[Workspace] = Relationship(back_populates="projects")
    runs: List["Run"] = Relationship(back_populates="project")
    user_id: str = Field(foreign_key="user.id")


# Runs
class RunResponse(SQLModel):
    name: str
    project_id: str = Field(foreign_key="project.id")


class Run(RunResponse, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    project: Optional[Project] = Relationship(back_populates="runs")
    user_id: str = Field(foreign_key="user.id")


SQLModel.metadata.create_all(engine)
