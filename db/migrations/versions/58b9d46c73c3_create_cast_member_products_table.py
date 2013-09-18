"""create_cast_member_products_table

Revision ID: 58b9d46c73c3
Revises: 242b0ae0146d
Create Date: 2013-09-18 06:12:04.692806

"""

# revision identifiers, used by Alembic.
revision = '58b9d46c73c3'
down_revision = '242b0ae0146d'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'cast_member_products',
        Column('cast_member_id', Integer(unsigned=True),
            ForeignKey('cast_members.cast_member_id',
            name='fk_cast_member_products_cast_member_id', ondelete="CASCADE"),
            index=True, nullable=False),
        Column('product_id', Integer(unsigned=True),
            ForeignKey('products.product_id',
            name='fk_cast_member_products_product_id', ondelete="CASCADE"),
            index=True, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('cast_member_products')
