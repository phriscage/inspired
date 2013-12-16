"""create_video_products_table

Revision ID: 17d5c118ae59
Revises: 707f5ea2eaf
Create Date: 2013-12-16 05:44:06.255301

"""

# revision identifiers, used by Alembic.
revision = '17d5c118ae59'
down_revision = '707f5ea2eaf'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'video_products',
        Column('video_id', Integer(unsigned=True),
            ForeignKey('videos.video_id',
            name='fk_video_products_video_id', ondelete="CASCADE"),
            index=True, nullable=False),
        Column('product_id', Integer(unsigned=True),
            ForeignKey('products.product_id',
            name='fk_video_products_product_id', ondelete="CASCADE"),
            index=True, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('video_products')
