"""create_product_images_table

Revision ID: c131b717b0a
Revises: 17d5c118ae59
Create Date: 2014-01-07 23:06:31.625858

"""

# revision identifiers, used by Alembic.
revision = 'c131b717b0a'
down_revision = '17d5c118ae59'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer, VARCHAR


def upgrade():
    op.create_table(
        'product_images',
        Column('product_image_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('url', String(length=2083), nullable=False),
        Column('product_id', Integer(unsigned=True), ForeignKey('products.product_id',
            name='fk_product_image_product_id', ondelete="CASCADE"), nullable=False),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('product_images')
