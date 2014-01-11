"""create_retailers_table

Revision ID: 242b0ae0146d
Revises: 50bca08c14c2
Create Date: 2013-09-18 06:10:00.573060

"""

# revision identifiers, used by Alembic.
revision = '242b0ae0146d'
down_revision = '50bca08c14c2'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'retailers', 
        Column('retailer_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('name', String(length=120), nullable=False),
        Column('url', String(length=255)),
        Column('image_url', String(length=2083)),
        Column('created_at', DateTime, nullable=False),
        Column('updated_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'

    )

def downgrade():
    op.drop_table('retailers')
