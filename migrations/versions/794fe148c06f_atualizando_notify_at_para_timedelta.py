"""atualizando notify_at para timedelta

Revision ID: 794fe148c06f
Revises: e1de12db14d6
Create Date: 2025-07-31 20:38:05.454287
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '794fe148c06f'
down_revision: Union[str, Sequence[str], None] = 'e1de12db14d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Converte integer (segundos) para interval
    op.execute(
        "ALTER TABLE task ALTER COLUMN notify_at TYPE INTERVAL USING notify_at * INTERVAL '1 second'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Converte interval para integer (segundos)
    op.execute(
        'ALTER TABLE task ALTER COLUMN notify_at TYPE INTEGER USING EXTRACT(EPOCH FROM notify_at)::integer'
    )


# ### end Alembic commands ###
