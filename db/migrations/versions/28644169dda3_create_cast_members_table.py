"""create_cast_members_table

Revision ID: 28644169dda3
Revises: 9a4b275976
Create Date: 2013-09-18 05:16:03.613338

"""

# revision identifiers, used by Alembic.
revision = '28644169dda3'
down_revision = '9a4b275976'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'cast_members',
        Column('cast_member_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('name', String(length=120), unique=True, index=True, nullable=False),
        Column('first_name', String(length=120)),
        Column('last_name', String(length=120)),
        Column('actor_first_name', String(length=120)),
        Column('actor_last_name', String(length=120)),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'

    )

def downgrade():
    op.drop_table('cast_members')
