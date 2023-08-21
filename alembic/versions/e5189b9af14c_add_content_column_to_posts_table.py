"""add content column to  posts table

Revision ID: e5189b9af14c
Revises: d824d13988d5
Create Date: 2023-08-21 17:37:21.744273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5189b9af14c'
down_revision: Union[str, None] = 'd824d13988d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
