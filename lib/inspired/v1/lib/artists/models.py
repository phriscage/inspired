""" the artists.models file contains the all the specific models """
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../lib')
from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import MapperExtension
from sqlalchemy.dialects.mysql import INTEGER
import datetime

class BaseExtension(MapperExtension):
    """Base entension class for all entity """

    def before_insert(self, mapper, connection, instance):
        """ set the created_at  """
        instance.created_at = datetime.datetime.now()

    def before_update(self, mapper, connection, instance):
        """ set the updated_at  """
        instance.updated_at = datetime.datetime.now()


class Artist(Base):
    """ Attributes for the Artist model. Custom MapperExtension declarative for 
        before insert and update methods. The migrate.versioning api does not
        handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True)
     """
    __tablename__ = 'artists'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('artist_id', INTEGER(unsigned=True), primary_key=True)
    name = Column(String(120), unique=True, index=True, nullable=False)
    first_name = Column(String(60))
    last_name = Column(String(60))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, name, first_name=None, last_name=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name

    #def __repr__(self):
        #return '<User %r>' % (self.name)

