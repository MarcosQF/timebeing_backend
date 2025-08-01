"""merge conflicting heads

Revision ID: a7b682f5ede5
Revises: 794fe148c06f, be5ff0adee55
Create Date: 2025-07-31 22:21:59.411271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b682f5ede5'
down_revision: Union[str, Sequence[str], None] = ('794fe148c06f', 'be5ff0adee55')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
