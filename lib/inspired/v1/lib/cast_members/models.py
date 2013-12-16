""" the cast_members.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
#from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import relationship, backref

""" cast_member_products join_table used to defined the bi-directional 
    relationship between CastMember and Product. Creating a separate class is 
    overkill unless additional atributes are required.
"""
cast_member_products = Table('cast_member_products', Base.metadata,
    Column('cast_member_id', Integer(unsigned=True), 
        ForeignKey('cast_members.cast_member_id',
        name='fk_cast_member_products_cast_member_id', ondelete="CASCADE"), 
        index=True, nullable=False),
    Column('product_id', Integer(unsigned=True), 
        ForeignKey('products.product_id',
        name='fk_cast_member_products_product_id', ondelete="CASCADE"), 
        index=True, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

class CastMember(Base):
    """ Attributes for the CastMember model. Custom MapperExtension declarative 
        for before insert and update methods. The migrate.versioning api does 
        not handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'cast_members'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('cast_member_id', Integer(unsigned=True), primary_key=True)
    name = Column(String(120), unique=True, index=True, nullable=False)
    first_name = Column(String(120))
    last_name = Column(String(120))
    actor_first_name = Column(String(120))
    actor_last_name = Column(String(120))
    products = relationship("Product", secondary="cast_member_products",
        backref="cast_members")
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, name, first_name=None, last_name=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name

    #def __repr__(self):
        #return '<User %r>' % (self.name)

