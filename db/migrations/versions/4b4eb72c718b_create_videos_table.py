"""create_videos_table

Revision ID: 4b4eb72c718b
Revises: 566a9de58431
Create Date: 2013-09-18 05:01:59.642485

"""

# revision identifiers, used by Alembic.
revision = '4b4eb72c718b'
down_revision = '566a9de58431'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'videos', 
        Column('video_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('name', String(length=120), unique=True, index=True, nullable=False),
        Column('image_url', String(length=2083)),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )


def downgrade():
    op.drop_table('videos')
