"""empty message

Revision ID: 6f5a0b015b02
Revises: 5f0418fbbb90
Create Date: 2019-10-31 19:49:18.280772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f5a0b015b02'
down_revision = '5f0418fbbb90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('activated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'activated')
    # ### end Alembic commands ###
