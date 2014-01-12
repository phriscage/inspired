""" the retailers.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
#from retailer_sources.models import RetailerSource
#from scenes.models import Scene
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.orm import relationship, backref

class Retailer(Base):
    """ Attributes for the Retailer model. Custom MapperExtension declarative for
        before insert and update methods. The migrate.versioning api does not
        handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'retailers'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('retailer_id', Integer(unsigned=True), primary_key=True)
    name = Column(String(120), nullable=False)
    url = Column(String(255))
    image_url = Column(String(2083))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, name, url, image_url):
        self.name = name
        self.url = url
        self.image_url = image_url

    #def __repr__(self):
        #return '<User %r>' % (self.name)

