import uuid

from pydantic import BaseModel, Field

from timebeing_backend.models.project import ProjectStatus
from timebeing_backend.schemas.task import TaskPublic


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    status: ProjectStatus = Field(default=ProjectStatus.criado)
    ai_context_text: str | None = None


class ProjectPublic(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    status: ProjectStatus


class ProjectList(BaseModel):
    projects: list[ProjectPublic]


class ProjectSoftUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectTasks(BaseModel):
    tasks: list[TaskPublic]


class ProjectStatusOption(BaseModel):
    value: str
    label: str
    description: str


class ProjectStatusOptions(BaseModel):
    status_options: list[ProjectStatusOption]
