"""seed_initial_product_data

Revision ID: 9e96ea4c385
Revises: c131b717b0a
Create Date: 2014-01-09 15:38:59.327265

"""

# revision identifiers, used by Alembic.
revision = '9e96ea4c385'
down_revision = 'c131b717b0a'

from alembic import op
from sqlalchemy import *
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../lib')
from inspired.v1.lib.products.models import Product
from inspired.v1.lib.product_images.models import ProductImage
import datetime


def upgrade():
    #Base.metadata.bind = op.get_bind()
    now = datetime.datetime.now()
    #for style in ['original', 'low_end', 'high_end']:
    op.execute(Product.__table__.insert().values(upc=123,brand='Paul Smith',
        model='striped beanie hat',ref_product_style_id=1,ref_product_type_id=1,
        created_at=now, updated_at=now))
    for url in [
        '/static/img/music/artists/austin-mahone/what-about-love/item-1.png',
        '/static/img/music/artists/austin-mahone/what-about-love/item-1-2.png',
        '/static/img/music/artists/austin-mahone/what-about-love/item-1-3.png',
        ]:
        op.execute(ProductImage.__table__.insert().values(
            url=url, product_id=1,
            created_at=now, updated_at=now))

def downgrade():
    op.execute("TRUNCATE %s" % Product.__table__)
    op.execute("TRUNCATE %s" % ProductImage.__table__)
