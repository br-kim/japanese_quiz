"""test2_migration_autogen

Revision ID: 007732ba2dd0
Revises: 75cb7aa9e962
Create Date: 2021-08-02 15:09:14.279303

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007732ba2dd0'
down_revision = '75cb7aa9e962'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('comment', 'created_at1')
    op.add_column('freeboard', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('freeboard', 'created_at1')
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('users', 'created_at1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at1', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column('users', 'created_at')
    op.add_column('freeboard', sa.Column('created_at1', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column('freeboard', 'created_at')
    op.add_column('comment', sa.Column('created_at1', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column('comment', 'created_at')
    # ### end Alembic commands ###
