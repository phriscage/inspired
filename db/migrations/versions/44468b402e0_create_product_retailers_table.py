"""create_product_retailers_table

Revision ID: 44468b402e0
Revises: 9e96ea4c385
Create Date: 2014-01-11 23:42:02.748285

"""

# revision identifiers, used by Alembic.
revision = '44468b402e0'
down_revision = '9e96ea4c385'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer, DECIMAL as Decimal


def upgrade():
    op.create_table(
        'product_retailers',
        Column('product_retailer_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('url', String(length=2083), nullable=False),
        Column('price', Decimal(10,2)),
        Column('product_id', Integer(unsigned=True), ForeignKey('products.product_id',
            name='fk_product_retailers_product_id', ondelete="CASCADE"), nullable=False),
        Column('retailer_id', Integer(unsigned=True), ForeignKey('retailers.retailer_id',
            name='fk_product_retailers_retailer_id', ondelete="CASCADE"), nullable=False),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('product_retailers')
