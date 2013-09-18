from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import INTEGER as Integer
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import db_session
from inspired.v1.lib.ref_product_types.models import RefProductType


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    rpt = RefProductType(name='original')
    rpt2 = RefProductType(name='low_cost')
    rpt3 = RefProductType(name='high_end')
    #meta.Session.add(rpt)
    db_session.add(rpt)
    db_session.add(rpt2)
    db_session.add(rpt3)
    db_session.commit()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    #migrate_engine.execute(RefProductType.__table__.delete())
    migrate_engine.execute("TRUNCATE %s" % RefProductType.__table__)
