from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from database import engine
from enum import Enum


##Enums
class TypeUser(Enum):
    PUBLIC = "PUBLIC"
    PROTECTED = "PROTECTED"


##AUth
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str


##User
class UserResponse(SQLModel):
    name: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True)
    password: Optional[str] = None
    user_type: TypeUser = Field(description="PUBLIC | PROTECTED")


class User(UserResponse, table=True):
    identifier: Optional[str] = Field(default=None, primary_key=True)
    workspaces: List["Workspace"] = Relationship(back_populates="user")


class UserLogin(BaseModel):
    id: str
    password: str


# Workspace
class WorkspaceResponse(SQLModel):
    name: str


class Workspace(WorkspaceResponse, table=True):
    identifier: Optional[str] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.identifier")
    user: Optional[User] = Relationship(back_populates="workspaces")
    projects: List["Project"] = Relationship(back_populates="workspace")


##Project
class ProjectResponse(SQLModel):
    name: str
    workspace_id: str = Field(foreign_key="workspace.identifier")


class Project(ProjectResponse, table=True):
    identifier: Optional[str] = Field(default=None, primary_key=True)

    workspace: Optional[Workspace] = Relationship(back_populates="projects")
    runs: List["Run"] = Relationship(back_populates="project")
    user_id: str = Field(foreign_key="user.identifier")


# Runs
class RunResponse(SQLModel):
    name: str
    project_id: str = Field(foreign_key="project.identifier")


class Run(RunResponse, table=True):
    identifier: Optional[str] = Field(default=None, primary_key=True)

    project: Optional[Project] = Relationship(back_populates="runs")
    user_id: str = Field(foreign_key="user.identifier")


SQLModel.metadata.create_all(engine)
