""" the artists.models file contains the all the specific models """
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../')
from lib.database import Base
from sqlalchemy import Column, Integer, String

class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, index=True, nullable=False)
    first_name = Column(String(60))
    last_name = Column(String(60))

    def __init__(self, name, first_name=None, last_name=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name

    #def __repr__(self):
        #return '<User %r>' % (self.name)

