"""create_scene_cast_members_table

Revision ID: 383fbb4fe7bd
Revises: 28644169dda3
Create Date: 2013-09-18 05:18:12.005798

"""

# revision identifiers, used by Alembic.
revision = '383fbb4fe7bd'
down_revision = '28644169dda3'

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'scene_cast_members', 
        Column('scene_id', Integer(unsigned=True), ForeignKey('scenes.scene_id',
            name='fk_scene_cast_members_scene_id', ondelete="CASCADE"), index=True,
            nullable=False),
        Column('cast_member_id', Integer(unsigned=True), ForeignKey('cast_members.cast_member_id',
            name='fk_scene_cast_members_cast_member_id', ondelete="CASCADE"), index=True,
            nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('scene_cast_members')
