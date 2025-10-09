"""обновлние таблицы задач

Revision ID: 3321afa9ac12
Revises: 3710f9f9c408
Create Date: 2025-10-09 16:17:04.604915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3321afa9ac12'
down_revision: Union[str, Sequence[str], None] = '3710f9f9c408'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
