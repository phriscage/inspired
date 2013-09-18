"""create_users_table

Revision ID: 4cd425e422fa
Revises: 58b9d46c73c3
Create Date: 2013-09-18 06:14:03.564533

"""

# revision identifiers, used by Alembic.
revision = '4cd425e422fa'
down_revision = '58b9d46c73c3'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'users', 
        Column('user_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('email_address', String(length=255), unique=True, index=True, nullable=False),
        Column('user_name', String(length=120), unique=True, index=True, nullable=False),
        Column('first_name', String(length=120)),
        Column('last_name', String(length=120)),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('users')
