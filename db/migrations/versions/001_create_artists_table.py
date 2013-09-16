from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import INTEGER


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
artists = Table('artists', post_meta,
    Column('artist_id', INTEGER(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), nullable=False),
    Column('first_name', String(length=60)),
    Column('last_name', String(length=60)),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artists'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artists'].drop()
