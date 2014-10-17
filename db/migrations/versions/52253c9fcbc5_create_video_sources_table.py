"""create_video_sources_table

Revision ID: 52253c9fcbc5
Revises: 1a490b503f0d
Create Date: 2013-09-18 05:12:29.146621

"""

# revision identifiers, used by Alembic.
revision = '52253c9fcbc5'
down_revision = '1a490b503f0d'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'video_sources',
        Column('video_source_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('name', String(length=120), nullable=False),
        Column('url', String(length=2083), nullable=False),
        Column('source_id', String(length=2083), nullable=False),
        Column('video_id', Integer(unsigned=True), ForeignKey('videos.video_id',
            name='fk_video_source_video_id', ondelete="CASCADE"), nullable=False),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('video_sources')
