import uuid
from enum import Enum

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timebeing_backend.models.task import Task

from ..database import Base
from .commom_mixins import TimestampMixin


class ProjectStatus(str, Enum):
    criado = 'Criado'
    andamento = 'Andamento'
    concluido = 'Concluído'


class ProjectPriorityState(str, Enum):
    baixa = 'Baixa'
    media = 'Média'
    alta = 'Alta'


@Base.mapped_as_dataclass
class Project(TimestampMixin):
    __tablename__ = 'project'

    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True)
    status: Mapped[ProjectStatus]
    ai_context_text: Mapped[str | None] = mapped_column(nullable=True)
    priority: Mapped[ProjectPriorityState] = mapped_column(
        default=ProjectPriorityState.baixa
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )

    tasks: Mapped[list['Task']] = relationship(
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )
