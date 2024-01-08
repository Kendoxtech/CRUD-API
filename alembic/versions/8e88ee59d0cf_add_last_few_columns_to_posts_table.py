"""add last few columns to posts table

Revision ID: 8e88ee59d0cf
Revises: a6fa2ebb3569
Create Date: 2024-01-07 20:40:52.155062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e88ee59d0cf'
down_revision: Union[str, None] = 'a6fa2ebb3569'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('post', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('post', 'published')
    op.drop_column('post','created_at')
    pass
