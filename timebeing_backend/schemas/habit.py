import uuid

from pydantic import BaseModel, Field


class HabitCreate(BaseModel):
    title: str
    description: str
    current_score: int = Field(ge=0, default=0)


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

