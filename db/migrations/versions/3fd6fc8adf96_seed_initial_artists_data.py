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
from inspired.v1.lib.videos.models import Video, video_products
from inspired.v1.lib.video_sources.models import VideoSource
from inspired.v1.lib.scenes.models import Scene
from inspired.v1.lib.cast_members.models import CastMember
import datetime

from string import lowercase

def upgrade():
    #Base.metadata.bind = op.get_bind()
    now = datetime.datetime.now()
    artists = [{
        'name': 'Austin Mahone', 
        'first_name': 'Austin', 
        'last_name': 'Mahone',
        'image_url': '/static/img/music/artists/austin-mahone/cover.png',
        'videos': [{
            'name': 'Austin Mahone - What About Love (Official Video)',
            'image_url': 'static/img/music/artists/austin-mahone/what-about-love.PNG',
            'video_source': {
                'name': 'youtube',
                'url': 'https://www.youtube.com/watch?v=2PEG82Udb90',
                'source_id': '2PEG82Udb90',
            }
        }, {
            'name': 'second video'
        }]
    }, {
        'name': 'Taylor Swift', 
        'first_name': 'Taylor', 
        'last_name': 'Swift',
        'image_url': '/static/img/music/artists/taylor-swift/cover.png',
        'videos': [{
            'name': 'Taylor Swift - I Knew You Were Trouble',
            'image_url': 'static/img/music/artists/taylor-swift/i-knew-you-were-trouble.PNG',
            'video_source': {
                'name': 'youtube',
                'url': 'https://www.youtube.com/watch?v=vNoKguSdy4YA',
                'source_id': 'vNoKguSdy4YA',
            }
        }]
    }, {
        'name': 'Demi Lovato', 
        'first_name': 'Demi', 
        'last_name': 'Lovato',
        'image_url': '/static/img/music/artists/demi-lovato/cover.png',
        'videos': [{
            'name': 'Demi Lovato - Give Your Heart a Break (Official Video)',
            'image_url': 'static/img/music/artists/demi-lovato/give-your-heart-a-break.png',
            'video_source': {
                'name': 'youtube',
                'url': 'https://www.youtube.com/watch?v=1zfzka5VwRc',
                'source_id': '1zfzka5VwRc'
            }
        }]
    }]
            
                
    video_id = 0
    for artist_idx, artist in enumerate(artists, 1):
        video_ids = []
        for video in artist['videos']:
            op.execute(Video.__table__.insert().values(
                created_at=now, updated_at=now, **video))
            video_id += 1
            video_ids.append(video_id)
            if 'video_source' in video:
                op.execute(VideoSource.__table__.insert().values(
                created_at=now, updated_at=now, video_id=video_id, **video['video_source']))
        op.execute(Artist.__table__.insert().values(
            created_at=now, updated_at=now, **artist))
        for video_id in video_ids:
            op.execute(artist_videos.insert().values(artist_id=artist_idx,
                video_id=video_id))

    ## products are only mapped to first video for now
    op.execute(video_products.insert().values(video_id=1, product_id=1))
    op.execute(video_products.insert().values(video_id=1, product_id=2))
    op.execute(video_products.insert().values(video_id=1, product_id=3))
    op.execute(video_products.insert().values(video_id=1, product_id=4))
        

def downgrade():
    op.execute("TRUNCATE %s" % Artist.__table__)
    op.execute("TRUNCATE %s" % Video.__table__)
    op.execute("TRUNCATE %s" % artist_videos)
