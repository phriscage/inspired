"""create_products_table

Revision ID: 50bca08c14c2
Revises: 2385b63bbe2d
Create Date: 2013-09-18 06:08:16.854194

"""

# revision identifiers, used by Alembic.
revision = '50bca08c14c2'
down_revision = '2385b63bbe2d'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer, DECIMAL as Decimal


def upgrade():
    op.create_table(
        'products',
        Column('product_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('upc', Decimal(12,0), unique=True, index=True, nullable=False),
        Column('brand', String(length=120), nullable=False),
        Column('model', String(length=120), nullable=False),
        Column('description', Text()),
        Column('ref_product_type_id', Integer(4, unsigned=True),
            ForeignKey('ref_product_types.ref_product_type_id',
            name='fk_scenes_ref_product_type_id', ondelete="CASCADE"),
            nullable=False),
        Column('ref_product_style_id', Integer(4, unsigned=True),
            ForeignKey('ref_product_styles.ref_product_style_id',
            name='fk_scenes_ref_product_style_id', ondelete="CASCADE"),
            nullable=False),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('products')
