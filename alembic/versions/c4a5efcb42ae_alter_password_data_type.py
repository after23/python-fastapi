"""alter password data type

Revision ID: c4a5efcb42ae
Revises: 4ae0aa92de30
Create Date: 2021-11-10 14:01:35.714981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4a5efcb42ae'
down_revision = '4ae0aa92de30'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'password', type_=sa.String())
    pass


def downgrade():
    op.alter_column('users', 'password', type_=sa.Integer())
    pass
