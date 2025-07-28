from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import UUID, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from ..database import Base
from .commom_mixins import TimestampMixin


class TaskPriorityState(str, Enum):
    baixa = 'Baixa'
    media = 'Média'
    alta = 'Alta'


@Base.mapped_as_dataclass
class Task(TimestampMixin):
    __tablename__ = 'task'

    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    scheduled_start_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    scheduled_end_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    priority: Mapped[TaskPriorityState]
    duration_estimate_blocks: Mapped[int | None] = mapped_column(nullable=True)
    location_text: Mapped[str | None] = mapped_column(nullable=True)
    location_lat: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True
    )
    location_lon: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True
    )
    ai_context_text: Mapped[str | None] = mapped_column(nullable=True)

    parent_task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('task.id'), nullable=True
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('project.id'), nullable=True
    )
    is_focus: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default='false', nullable=False
    )
    status: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default='false', nullable=False
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )

    pai: Mapped[Task | None] = relationship(
        'Task', back_populates='subtasks', remote_side=[id], init=False
    )

    subtasks: Mapped[list[Task]] = relationship(
        'Task', back_populates='pai', cascade='all, delete-orphan', init=False
    )
