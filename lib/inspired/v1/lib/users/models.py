""" the users.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
#from inspired.v1.lib.videos.models import Video
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
#from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import relationship, backref


class User(Base):
    """ Attributes for the User model. Custom MapperExtension declarative for 
        before insert and update methods. The migrate.versioning api does not
        handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'users'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('user_id', Integer(unsigned=True), primary_key=True)
    email_address = Column(String(255), unique=True, index=True, nullable=False)
    user_name = Column(String(120), unique=True, index=True, nullable=False)
    first_name = Column(String(120))
    last_name = Column(String(120))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, email_address, user_name=None, first_name=None, 
        last_name=None):
        self.email_address = name
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name

    #def __repr__(self):
        #return '<User %r>' % (self.name)

