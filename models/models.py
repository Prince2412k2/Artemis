from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import EmailStr
from database import engine


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    identifier: str = Field(unique=True)
    name: str
    email: EmailStr = Field(unique=True)
    workspaces: List["Workspace"] = Relationship(back_populates="user")


class Workspace(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    identifier: str = Field(unique=True)
    name: str
    user_id: int = Field(foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="workspaces")
    projects: List["Project"] = Relationship(back_populates="workspace")


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    identifier: str = Field(unique=True)
    name: str
    workspace_id: int = Field(foreign_key="workspace.id")

    workspace: Optional[Workspace] = Relationship(back_populates="projects")
    runs: List["Run"] = Relationship(back_populates="project")


class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    identifier: str = Field(unique=True)
    name: str
    project_id: int = Field(foreign_key="project.id")

    project: Optional[Project] = Relationship(back_populates="runs")


SQLModel.metadata.create_all(engine)
