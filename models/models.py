from sqlmodel import SQLModel, Field, Relationship,UniqueConstraint
from typing import Optional, List
from pydantic import BaseModel, EmailStr
import uuid
from database import engine  # Assuming the database engine is defined here

## Auth Models
class Token(BaseModel):
    access_token: str
    token_type: str

## User Models
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

## Workspace Models
class WorkspaceResponse(SQLModel):
    name: str

class Workspace(WorkspaceResponse, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")  # Ensure UUID consistency
    user: Optional[User] = Relationship(back_populates="workspaces")
    projects: List["Project"] = Relationship(back_populates="workspace")

    # Ensure unique workspace names per user
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="workspace_user_unique"),
    )

## Project Models
class ProjectResponse(SQLModel):
    name: str
    workspace_id: uuid.UUID = Field(foreign_key="workspace.id")  # Ensure UUID consistency

class Project(ProjectResponse, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    workspace_id: uuid.UUID = Field(foreign_key="workspace.id")  # Ensure UUID consistency
    user_id: uuid.UUID = Field(foreign_key="user.id")  # Ensure UUID consistency
    workspace: Optional[Workspace] = Relationship(back_populates="projects")
    runs: List["Run"] = Relationship(back_populates="project")

    # Ensure unique project names per workspace
    __table_args__ = (
        UniqueConstraint("name", "workspace_id", name="project_workspace_unique"),
    )

## Run Models
class RunResponse(SQLModel):
    name: str
    project_id: uuid.UUID = Field(foreign_key="project.id")  # Ensure UUID consistency

class Run(RunResponse, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID = Field(foreign_key="project.id")  # Ensure UUID consistency
    user_id: uuid.UUID = Field(foreign_key="user.id")  # Ensure UUID consistency
    project: Optional[Project] = Relationship(back_populates="runs")

# Create tables
SQLModel.metadata.create_all(engine)
