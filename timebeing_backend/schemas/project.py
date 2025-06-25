import uuid

from pydantic import BaseModel, Field

from timebeing_backend.models.project import ProjectStatus


class ProjectCreate(BaseModel):
    title: str
    description: str | None
    status: ProjectStatus = Field(default=ProjectStatus.criado)
    ai_context_text: str | None


class ProjectPublic(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: ProjectStatus


class ProjectList(BaseModel):
    projects: list[ProjectPublic]


class ProjectSoftUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
