"""add column comment table

Revision ID: 8f62bd82e81b
Revises: 007732ba2dd0
Create Date: 2021-08-03 17:08:28.315323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f62bd82e81b'
down_revision = '007732ba2dd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('parent_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'parent_id')
    # ### end Alembic commands ###