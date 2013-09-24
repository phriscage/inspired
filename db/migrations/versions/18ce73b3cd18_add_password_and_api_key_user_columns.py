"""add password and api_key user columns

Revision ID: 18ce73b3cd18
Revises: 4cd425e422fa
Create Date: 2013-09-24 16:40:33.357813

"""

# revision identifiers, used by Alembic.
revision = '18ce73b3cd18'
down_revision = '4cd425e422fa'

from alembic import op
from sqlalchemy import *

def upgrade():
    #Base.metadata.bind = op.get_bind()
    op.add_column('users', Column('password', String(length=120)))
    op.add_column('users', Column('api_key', String(length=40)))

def downgrade():
    op.drop_column('users', 'password')
    op.drop_column('users', 'api_key')
