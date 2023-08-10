"""add column to user table

Revision ID: 88ef91e08015
Revises: 249c045b5377
Create Date: 2023-08-10 19:20:26.915521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88ef91e08015'
down_revision = '249c045b5377'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('permission', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'permission')
    # ### end Alembic commands ###