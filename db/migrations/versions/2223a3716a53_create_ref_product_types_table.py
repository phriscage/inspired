"""create_ref_product_types_table

Revision ID: 2223a3716a53
Revises: 383fbb4fe7bd
Create Date: 2013-09-18 05:19:32.306226

"""

# revision identifiers, used by Alembic.
revision = '2223a3716a53'
down_revision = '383fbb4fe7bd'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'ref_product_types', 
        Column('ref_product_type_id', Integer(4, unsigned=True),
            primary_key=True, nullable=False),
        Column('name', String(length=60), unique=True, nullable=False),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'

    )

def downgrade():
    op.drop_table('ref_product_types')
