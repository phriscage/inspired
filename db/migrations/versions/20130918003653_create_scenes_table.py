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

scenes = Table('scenes', post_meta,
    Column('scene_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), nullable=False),
    Column('start_time', Time, nullable=False, default=ColumnDefault('00:00:00')),
    Column('end_time', Time, nullable=False, default=ColumnDefault('00:00:00')),
    Column('video_id', Integer(unsigned=True), ForeignKey('videos.video_id',
        name='fk_scenes_video_id', ondelete="CASCADE"), nullable=False),
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
    post_meta.tables['scenes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['scenes'].drop()
