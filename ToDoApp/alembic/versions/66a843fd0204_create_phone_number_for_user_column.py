"""Create phone number for user column

Revision ID: 66a843fd0204
Revises: 
Create Date: 2025-05-28 15:56:01.228607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66a843fd0204'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
    pass
