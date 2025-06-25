import uuid

from pydantic import BaseModel, Field


class HabitCreate(BaseModel):
    title: str
    description: str | None = None
    current_score: int | None = Field(ge=0, default=None)


class HabitPublic(HabitCreate):
    id: uuid.UUID


class HabitList(BaseModel):
    habits: list[HabitPublic]


class HabitSoftUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    current_score: int | None = None


class Message(BaseModel):
    message: str
