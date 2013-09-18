from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cast_members = Table('cast_members', post_meta,
    Column('cast_member_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), unique=True, index=True, nullable=False),
    Column('first_name', String(length=120)),
    Column('last_name', String(length=120)),
    Column('actor_first_name', String(length=120)),
    Column('actor_last_name', String(length=120)),
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
        name='fk_scenes_video_id', ondelete="CASCADE"), index=True, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

scene_cast_members = Table('scene_cast_members', post_meta,
    Column('scene_id', Integer(unsigned=True), ForeignKey('scenes.scene_id',
        name='fk_scene_cast_members_scene_id', ondelete="CASCADE"), index=True,
        nullable=False),
    Column('cast_member_id', Integer(unsigned=True), ForeignKey('cast_members.cast_member_id',
        name='fk_scene_cast_members_cast_member_id', ondelete="CASCADE"), index=True,
        nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['scene_cast_members'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['scene_cast_members'].drop()
