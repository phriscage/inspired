"""seed_ref_product_styles_table

Revision ID: 2385b63bbe2d
Revises: 1574bad317a2
Create Date: 2013-09-18 06:00:26.651993

"""

# revision identifiers, used by Alembic.
revision = '2385b63bbe2d'
down_revision = '1574bad317a2'

from alembic import op
from sqlalchemy import *
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../lib')
from inspired.v1.lib.ref_product_styles.models import RefProductStyle
import datetime


def upgrade():
    #Base.metadata.bind = op.get_bind()
    now = datetime.datetime.now()
    for style in ['shirt', 'jeans', 'dress', 'jacket', 'show']:
        op.execute(RefProductStyle.__table__.insert().values(name=style,
            created_at=now, updated_at=now))

def downgrade():
    op.execute("TRUNCATE %s" % RefProductStyle.__table__)
