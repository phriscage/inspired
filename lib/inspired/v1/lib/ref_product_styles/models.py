""" the ref_product_styles.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import INTEGER as Integer
from sqlalchemy.orm import relationship, backref

class RefProductStyle(Base):
    """ Attributes for the RefProductStyle model. Custom MapperExtension declarative
        for before insert and update methods. The migrate.versioning api does
        not handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'ref_product_styles'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('ref_product_style_id', Integer(4, unsigned=True), primary_key=True)
    name = Column(String(60), unique=True, nullable=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, name):
        self.name = name

    #def __repr__(self):
        #return '<User %r>' % (self.name)

