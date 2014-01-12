"""seed_initial_product_retailer_data

Revision ID: 653ed798dd4
Revises: 44468b402e0
Create Date: 2014-01-12 00:59:21.677537

"""

# revision identifiers, used by Alembic.
revision = '653ed798dd4'
down_revision = '44468b402e0'

from alembic import op
from sqlalchemy import *
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../lib')
from inspired.v1.lib.retailers.models import Retailer
from inspired.v1.lib.product_retailers.models import ProductRetailer
import datetime


def upgrade():
    #Base.metadata.bind = op.get_bind()
    now = datetime.datetime.now()
    #for style in ['original', 'low_end', 'high_end']:
    op.execute(Retailer.__table__.insert().values(name="Abc",
        url="http://abc.com",image_url="http://abc.com/abc.png",
        created_at=now, updated_at=now))
    op.execute(ProductRetailer.__table__.insert().values(
        url="http://abc.com?asdfs", price="1.23", retailer_id=1, product_id=1,
        created_at=now, updated_at=now))

def downgrade():
    op.execute("TRUNCATE %s" % Retailer.__table__)
    op.execute("TRUNCATE %s" % ProductRetailer.__table__)
