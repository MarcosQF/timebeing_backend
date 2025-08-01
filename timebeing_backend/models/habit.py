import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .commom_mixins import TimestampMixin


@Base.mapped_as_dataclass
class Habit(TimestampMixin):
    __tablename__ = 'habit'

    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    current_score: Mapped[int] = mapped_column(nullable=True)
    ai_context_prompt: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[str] = mapped_column(nullable=False)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
