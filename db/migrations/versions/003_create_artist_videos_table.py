from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import INTEGER as Integer
## need for ForeignKey relationship creation on artist_videos
#from inspired.v1.lib.artists.models import Artist
#from inspired.v1.lib.videos.models import Video



from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
## need for ForeignKey relationship creation on artist_videos
artists = Table('artists', post_meta,
    Column('artist_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), unique=True, index=True, nullable=False),
    Column('first_name', String(length=60)),
    Column('last_name', String(length=60)),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)
videos = Table('videos', post_meta,
    Column('video_id', Integer(unsigned=True), primary_key=True, nullable=False),
    Column('name', String(length=120), unique=True, index=True, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('updated_at', DateTime, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

artist_videos = Table('artist_videos', post_meta,
    Column('artist_id', Integer(unsigned=True), ForeignKey('artists.artist_id',
        name='fk_artist_videos_artist_id', ondelete="CASCADE"), index=True, 
        nullable=False),
    Column('video_id', Integer(unsigned=True), ForeignKey('videos.video_id',
        name='fk_artist_videos_video_id', ondelete="CASCADE"), index=True, 
        nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_videos'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_videos'].drop()
