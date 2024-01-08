"""add foreign-key to posts table

Revision ID: a6fa2ebb3569
Revises: 370ee0145f08
Create Date: 2024-01-07 20:25:33.544777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6fa2ebb3569'
down_revision: Union[str, None] = '370ee0145f08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table="post", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name="post")
    op.drop_column('post', 'owner_id')
    pass
