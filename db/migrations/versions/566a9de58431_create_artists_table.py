"""create_artists_table

Revision ID: 566a9de58431
Revises: None
Create Date: 2013-09-18 04:57:04.750823

"""

# revision identifiers, used by Alembic.
revision = '566a9de58431'
down_revision = None

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER


def upgrade():
    op.create_table(
        'artists',
        Column('artist_id', INTEGER(unsigned=True), primary_key=True, nullable=False),
        Column('name', String(length=120), unique=True, index=True, nullable=False),
        Column('first_name', String(length=60)),
        Column('last_name', String(length=60)),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )


def downgrade():
    op.drop_table('artists')
