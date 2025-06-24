import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import UUID, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime

from ..database import Base
from .commom_mixins import TimestampMixin


class StatusState(str, Enum):
    aberta = 'Aberta'
    andamento = 'Andamento'
    concluida = 'Concluída'


class PriorityState(str, Enum):
    baixa = 'Baixa'
    media = 'Média'
    alta = 'Alta'


@Base.mapped_as_dataclass
class Task(TimestampMixin):
    __tablename__ = 'task'

    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[StatusState]
    priority: Mapped[PriorityState]
    duration_estimate_blocks: Mapped[int | None] = mapped_column(nullable=True)
    location_text: Mapped[str | None] = mapped_column(nullable=True)
    location_lat: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True
    )
    location_lon: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True
    )
    ai_context_text: Mapped[str | None] = mapped_column(nullable=True)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        init=False
    )
