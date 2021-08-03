"""test_migration_autogen

Revision ID: 75cb7aa9e962
Revises: 1a575075ae05
Create Date: 2021-08-02 15:07:49.853902

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '75cb7aa9e962'
down_revision = '1a575075ae05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('created_at1', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('comment', 'created_at')
    op.add_column('freeboard', sa.Column('created_at1', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('freeboard', 'created_at')
    op.add_column('users', sa.Column('created_at1', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('users', 'created_at1')
    op.add_column('freeboard', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('freeboard', 'created_at1')
    op.add_column('comment', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('comment', 'created_at1')
    # ### end Alembic commands ###