"""add user_id to all models

Revision ID: be5ff0adee55
Revises: 2656ac15afd5
Create Date: 2025-07-30 23:54:11.075076
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be5ff0adee55'
down_revision: Union[str, Sequence[str], None] = '2656ac15afd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add user_id column to task table
    op.add_column(
        'task',
        sa.Column('user_id', sa.String(), nullable=False, server_default=''),
    )

    # Add user_id column to project table
    op.add_column(
        'project',
        sa.Column('user_id', sa.String(), nullable=False, server_default=''),
    )

    # Add user_id column to habit table
    op.add_column(
        'habit',
        sa.Column('user_id', sa.String(), nullable=False, server_default=''),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove user_id column from habit table
    op.drop_column('habit', 'user_id')

    # Remove user_id column from project table
    op.drop_column('project', 'user_id')

    # Remove user_id column from task table
    op.drop_column('task', 'user_id')
