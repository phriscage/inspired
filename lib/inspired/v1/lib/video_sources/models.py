""" the video_sources.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.orm import relationship, backref

class VideoSource(Base):
    """ Attributes for the VideoSource model. Custom MapperExtension declarative
        for before insert and update methods. The migrate.versioning api does
        not handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'video_sources'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('video_source_id', Integer(unsigned=True), primary_key=True)
    name = Column(String(120), nullable=False)
    url = Column(String(length=2083), nullable=False)
    source_id = Column(String(length=2083), nullable=False)
    video_id = Column('video_id', Integer(unsigned=True),
        ForeignKey('videos.video_id', name='fk_video_sources_video_id',
        ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    #def __init__(self, name, url, video):
        #self.name = name
        #self.url = url
        #self.video = video

    #def __repr__(self):
        #return '<User %r>' % (self.name)

