""" the users.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
import uuid
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
#from inspired.v1.lib.videos.models import Video
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
#from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import relationship, backref
from werkzeug import generate_password_hash, check_password_hash


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
    user_name = Column(String(120), unique=True, index=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    password = Column(String(120))
    api_key = Column(String(40))
    facebook_id = Column(String(120))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, email_address, password=None, user_name=None,
        first_name=None, last_name=None, facebook_id=None):
        self.email_address = email_address
        if password:
            self.set_password(password)
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.facebook_id = facebook_id
        self.set_api_key()

    def set_password(self, password):
        """ set the password using werkzeug generate_password_hash """
        self.password = generate_password_hash(password)
   
    def check_password(self, password):
        """ check the password using werkzeug check_password_hash """
        if not self.password:
            return None
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        """ should just return True unless the object represents a user 
            that should not be allowed to authenticate for some reason.
        """
        return True

    def set_api_key(self):
        """ set the api_key based on the host ID and current time """
        self.api_key = str(uuid.uuid1())
   
    def is_active(self):
        """ method should return True for users unless they are inactive, for 
            example because they have been banned.
        """
        return True

    def is_anonymous(self):
        """ method should return True only for fake users that are not supposed 
            to log in to the system.
        """
        return False

    def get_id(self):
        """ method should return a unique identifier for the user, in unicode 
            format. We use the unique id generated by the database layer for 
            this.
        """
        return unicode(self.id)

    #def __repr__(self):
        #return '<User %r>' % (self.name)

