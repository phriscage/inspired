from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
videos = Table('videos', post_meta,
    Column('video_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

video_sources = Table('video_sources', post_meta,
    Column('video_source_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), nullable=False),
    Column('url', String(length=120), unique=True, nullable=False),
    Column('video_id', Integer(unsigned=True), ForeignKey('videos.video_id',
        name='fk_video_source_video_id', ondelete="CASCADE"), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['video_sources'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['video_sources'].drop()
