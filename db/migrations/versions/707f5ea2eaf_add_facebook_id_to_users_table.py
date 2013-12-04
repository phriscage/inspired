"""add_facebook_id_to_users_table

Revision ID: 707f5ea2eaf
Revises: 18ce73b3cd18
Create Date: 2013-12-04 08:14:18.129482

"""

# revision identifiers, used by Alembic.
revision = '707f5ea2eaf'
down_revision = '18ce73b3cd18'

from alembic import op
from sqlalchemy import *


def upgrade():
    op.add_column('users', Column('facebook_id', String(120)))


def downgrade():
    op.drop_column('users', 'facebook_id')
