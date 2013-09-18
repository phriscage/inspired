"""create_scenes_table

Revision ID: 9a4b275976
Revises: 52253c9fcbc5
Create Date: 2013-09-18 05:14:12.292139

"""

# revision identifiers, used by Alembic.
revision = '9a4b275976'
down_revision = '52253c9fcbc5'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'scenes', 
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

def downgrade():
    op.drop_table('scenes')
