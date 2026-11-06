"""alter project media url to text

Revision ID: e41a87b1c312
Revises: 9bfc3e471536
Create Date: 2026-11-06 17:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e41a87b1c312'
down_revision: Union[str, Sequence[str], None] = '9bfc3e471536'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'project_media',
        'url',
        existing_type=sa.String(length=500),
        type_=sa.Text(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'project_media',
        'url',
        existing_type=sa.Text(),
        type_=sa.String(length=500),
        existing_nullable=False,
    )
