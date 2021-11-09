"""add last few column to posts table

Revision ID: 85e5882b47ff
Revises: bc7cd04d7c7c
Create Date: 2021-11-09 10:09:01.075515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85e5882b47ff'
down_revision = 'bc7cd04d7c7c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
