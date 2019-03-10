"""new user field

Revision ID: 0ce49cf3ffc5
Revises: 39f3120b1531
Create Date: 2019-03-10 10:43:39.116894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ce49cf3ffc5'
down_revision = '39f3120b1531'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    # ### end Alembic commands ###
