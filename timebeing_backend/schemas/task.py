import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from timebeing_backend.models.task import TaskPriorityState, TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None
    due_date: datetime | None
    status: TaskStatus = Field(default=TaskStatus.aberta)
    priority: TaskPriorityState = Field(default=TaskPriorityState.baixa)
    duration_estimate_blocks: int | None
    location_text: str | None
    location_lat: Decimal | None
    location_lon: Decimal | None
    ai_context_text: str | None


class TaskPublic(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    due_date: datetime
    status: TaskStatus
    priority: TaskPriorityState
    duration_estimate_blocks: int
    location_text: str
    location_lat: Decimal
    location_lon: Decimal


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskSoftUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    status: TaskStatus | None = None
    priority: TaskPriorityState | None = None
    duration_estimate_blocks: int | None = None
    location_text: str | None = None
    location_lat: Decimal | None = None
    location_lon: Decimal | None = None
    ai_context_text: str | None = None
