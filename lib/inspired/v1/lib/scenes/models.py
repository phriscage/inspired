""" the scenes.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
#from cast_members.models import CastMember
from sqlalchemy import Column, String, DateTime, Time, ForeignKey, Index, Table
from sqlalchemy.dialects.mysql import INTEGER as Integer
#from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import relationship, backref


""" scene_cast_members join_table used to defined the bi-directional relationship
    between Scene and CastMember. Creating a separate class is overkill unless
    additional atributes are required.
"""
scene_cast_members = Table('scene_cast_members', Base.metadata,
    Column('scene_id', Integer(unsigned=True), ForeignKey('scenes.scene_id',
        name='fk_scene_cast_members_scene_id', ondelete="CASCADE"), index=True,
        nullable=False),
    Column('cast_member_id', Integer(unsigned=True), ForeignKey('cast_members.cast_member_id',
        name='fk_scene_cast_members_cast_member_id', ondelete="CASCADE"), index=True,
        nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

class Scene(Base):
    """ Attributes for the Scene model. Custom MapperExtension declarative for 
        before insert and update methods. The migrate.versioning api does not
        handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'scenes'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('scene_id', Integer(unsigned=True), primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    start_time = Column(Time(), nullable=False, default='00:00:00')
    end_time = Column(Time(), nullable=False, default='00:00:00')
    video_id = Column('video_id', Integer(unsigned=True), 
        ForeignKey('videos.video_id', name='fk_scenes_video_id', 
        ondelete="CASCADE"), index=True, nullable=False)
    cast_members = relationship("CastMember", secondary="scene_cast_members", 
        backref="scenes")
    #products = relationship("Product", backref="products")
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    #def __repr__(self):
        #return '<User %r>' % (self.name)

