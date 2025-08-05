import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class HabitCreate(BaseModel):
    title: str
    description: str | None = None
    current_score: int | None = Field(ge=0, default=None)
    ai_context_prompt: str | None = None


class HabitPublic(HabitCreate):
    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime


class HabitList(BaseModel):
    habits: list[HabitPublic]


class HabitSoftUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    current_score: int | None = None
    ai_context_prompt: str | None = None


class Message(BaseModel):
    message: str
