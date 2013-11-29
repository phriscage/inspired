"""seed_ref_product_types_table

Revision ID: 1574bad317a2
Revises: 3c25ee1135be
Create Date: 2013-09-18 05:24:26.755739

"""

# revision identifiers, used by Alembic.
revision = '1574bad317a2'
down_revision = '3c25ee1135be'

from alembic import op
from sqlalchemy import *
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../lib')
from inspired.v1.lib.ref_product_types.models import RefProductType
import datetime


def upgrade():
    #Base.metadata.bind = op.get_bind()
    now = datetime.datetime.now()
    for type in ['shirt', 'jeans', 'dress', 'jacket', 'show']:
        op.execute(RefProductType.__table__.insert().values(name=type,
            created_at=now, updated_at=now))

def downgrade():
    op.execute("TRUNCATE %s" % RefProductType.__table__)
