"""seed_initial_artists_data

Revision ID: 3fd6fc8adf96
Revises: 653ed798dd4
Create Date: 2014-02-01 19:57:09.422096

"""

# revision identifiers, used by Alembic.
revision = '3fd6fc8adf96'
down_revision = '653ed798dd4'

from alembic import op
from sqlalchemy import *
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../lib')
from inspired.v1.lib.artists.models import Artist, artist_videos
from inspired.v1.lib.videos.models import Video
from inspired.v1.lib.video_sources.models import VideoSource
from inspired.v1.lib.scenes.models import Scene
from inspired.v1.lib.cast_members.models import CastMember
import datetime

from string import lowercase

def upgrade():
    #Base.metadata.bind = op.get_bind()
    now = datetime.datetime.now()
    op.execute(Video.__table__.insert().values(name='first video'))
    op.execute(Video.__table__.insert().values(name='second video'))
    for i,l in enumerate(lowercase):
        op.execute(Artist.__table__.insert().values(name=lowercase[i:i+3],
            first_name=lowercase[i],
            last_name=lowercase[i:i+2],
            #image_url="/static/img/music/artists/austin-mahone/what-about-love/item-1.png",
            image_url="/static/img/music/artists/%s.png" % lowercase[i:i+3],
            created_at=now, updated_at=now))
        op.execute(artist_videos.insert().values(artist_id=i+1, 
            video_id=1))
        op.execute(artist_videos.insert().values(artist_id=i+1, 
            video_id=2))

def downgrade():
    op.execute("TRUNCATE %s" % Artist.__table__)
    op.execute("TRUNCATE %s" % Video.__table__)
    op.execute("TRUNCATE %s" % artist_videos)
