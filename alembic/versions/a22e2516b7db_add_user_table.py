"""add user table

Revision ID: a22e2516b7db
Revises: 84b226002921
Create Date: 2021-11-09 09:46:19.301344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a22e2516b7db'
down_revision = '84b226002921'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('email', sa.String(), nullable=False), 
                    sa.Column('password', sa.Integer(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), 
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
