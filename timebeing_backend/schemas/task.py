import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator

from timebeing_backend.models.task import TaskPriorityState


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    notify_at: timedelta | None = None
    scheduled_start_time: datetime | None = None
    scheduled_end_time: datetime | None = None
    status: bool = Field(default=False)
    priority: TaskPriorityState = Field(default=TaskPriorityState.baixa)
    duration_estimate_blocks: int | None = None
    location_text: str | None = None
    location_lat: Decimal | None = None
    location_lon: Decimal | None = None
    ai_context_text: str | None = None
    is_focus: bool = Field(default=False)
    parent_task_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None

    @field_validator('due_date', mode='before')
    def ensure_brazil_timezone(cls, v):
        if v is None:
            return v

        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        if v.tzinfo:
            return v.astimezone(ZoneInfo('America/Sao_Paulo'))

        return v.replace(tzinfo=ZoneInfo('America/Sao_Paulo'))


class TaskPublic(BaseModel):
    id: uuid.UUID
    title: str
    parent_task_id: uuid.UUID | None
    project_id: uuid.UUID | None
    user_id: str
    description: str | None
    due_date: datetime | None
    notify_at: timedelta | None
    scheduled_start_time: datetime | None
    scheduled_end_time: datetime | None
    status: bool
    priority: TaskPriorityState
    duration_estimate_blocks: int | None
    location_text: str | None
    location_lat: Decimal | None
    location_lon: Decimal | None
    ai_context_text: str | None
    is_focus: bool
    created_at: datetime
    updated_at: datetime

    @field_validator('due_date', mode='before')
    def ensure_brazil_timezone(cls, v):
        if v is None:
            return v

        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        if v.tzinfo:
            return v.astimezone(ZoneInfo('America/Sao_Paulo'))

        return v.replace(tzinfo=ZoneInfo('America/Sao_Paulo'))


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskSoftUpdate(BaseModel):
    title: str | None = None
    parent_task_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    description: str | None = None
    due_date: datetime | None = None
    notify_at: timedelta | None = None
    scheduled_start_time: datetime | None = None
    scheduled_end_time: datetime | None = None
    status: bool | None = None
    priority: TaskPriorityState | None = None
    duration_estimate_blocks: int | None = None
    location_text: str | None = None
    location_lat: Decimal | None = None
    location_lon: Decimal | None = None
    ai_context_text: str | None = None
    is_focus: bool | None = None

    @field_validator('due_date', mode='before')
    def ensure_brazil_timezone(cls, v):
        if v is None:
            return v

        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        if v.tzinfo:
            return v.astimezone(ZoneInfo('America/Sao_Paulo'))

        return v.replace(tzinfo=ZoneInfo('America/Sao_Paulo'))
