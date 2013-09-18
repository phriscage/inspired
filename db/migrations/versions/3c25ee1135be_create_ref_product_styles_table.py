"""create_ref_product_styles_table

Revision ID: 3c25ee1135be
Revises: 2223a3716a53
Create Date: 2013-09-18 05:21:07.215621

"""

# revision identifiers, used by Alembic.
revision = '3c25ee1135be'
down_revision = '2223a3716a53'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'ref_product_styles', 
        Column('ref_product_style_id', Integer(4, unsigned=True),
            primary_key=True, nullable=False),
        Column('name', String(length=60), unique=True, nullable=False),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('ref_product_styles')
