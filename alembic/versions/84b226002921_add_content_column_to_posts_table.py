"""add content column to posts table

Revision ID: 84b226002921
Revises: d88556719374
Create Date: 2021-11-09 09:39:17.010858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84b226002921'
down_revision = 'd88556719374'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
