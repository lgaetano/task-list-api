"""Remove is_complete column

Revision ID: 0b2d3a36227b
Revises: 1451bf391041
Create Date: 2021-10-29 10:37:59.009652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b2d3a36227b'
down_revision = '1451bf391041'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'is_complete')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_complete', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
