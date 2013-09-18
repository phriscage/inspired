"""create_artist_videos_table

Revision ID: 1a490b503f0d
Revises: 4b4eb72c718b
Create Date: 2013-09-18 05:06:06.564602

"""

# revision identifiers, used by Alembic.
revision = '1a490b503f0d'
down_revision = '4b4eb72c718b'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'artist_videos', 
        Column('artist_id', Integer(unsigned=True), ForeignKey('artists.artist_id',
            name='fk_artist_videos_artist_id', ondelete="CASCADE"), index=True,
            nullable=False),
        Column('video_id', Integer(unsigned=True), ForeignKey('videos.video_id',
            name='fk_artist_videos_video_id', ondelete="CASCADE"), index=True,
            nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'

    )

def downgrade():
    op.drop_table('artist_videos')
