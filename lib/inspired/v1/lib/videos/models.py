""" the videos.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
#from video_sources.models import VideoSource
#from scenes.models import Scene
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.orm import relationship, backref

""" video_products join_table used to defined the bi-directional
    relationship between Video and Product. Creating a separate class is
    overkill unless additional atributes are required.
"""
video_products = Table('video_products', Base.metadata,
    Column('video_id', Integer(unsigned=True),
        ForeignKey('videos.video_id',
        name='fk_video_products_video_id', ondelete="CASCADE"),
        index=True, nullable=False),
    Column('product_id', Integer(unsigned=True),
        ForeignKey('products.product_id',
        name='fk_video_products_product_id', ondelete="CASCADE"),
        index=True, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

class Video(Base):
    """ Attributes for the Video model. Custom MapperExtension declarative for 
        before insert and update methods. The migrate.versioning api does not
        handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'videos'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('video_id', Integer(unsigned=True), primary_key=True)
    name = Column(String(120), unique=True, index=True, nullable=False)
    image_url = Column(String(2083))
    video_sources = relationship("VideoSource", backref="video")
    scenes = relationship("Scene", backref="video")
    products = relationship("Product", secondary="video_products",
        backref="videos")
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, name, products=[]):
        self.name = name
        self.products = products

    #def __repr__(self):
        #return '<User %r>' % (self.name)

