""" the artists.models file contains the all the specific models """
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from helpers import BaseExtension
#from videos.models import Video
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
#from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import relationship, backref


""" artist_videos join_table used to defined the bi-directional relationship
    between Artist and Video. Creating a separate class is overkill unless
    additional atributes are required.
"""
artist_videos = Table('artist_videos', Base.metadata,
    Column('artist_id', Integer(unsigned=True), ForeignKey('artists.artist_id',
        name='fk_artist_videos_artist_id', ondelete="CASCADE"), index=True,
        nullable=False),
    Column('video_id', Integer(unsigned=True), ForeignKey('videos.video_id',
        name='fk_artist_videos_video_id', ondelete="CASCADE"), index=True,
        nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

    
class Artist(Base):
    """ Attributes for the Artist model. Custom MapperExtension declarative for 
        before insert and update methods. The migrate.versioning api does not
        handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'artists'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('artist_id', Integer(unsigned=True), primary_key=True)
    name = Column(String(120), unique=True, index=True, nullable=False)
    first_name = Column(String(60))
    last_name = Column(String(60))
    videos = relationship("Video", secondary="artist_videos", backref="artists")
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, name, first_name=None, last_name=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name

    #def __repr__(self):
        #return '<User %r>' % (self.name)

