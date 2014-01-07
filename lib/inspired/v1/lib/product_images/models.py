""" the product_images.models file contains the all the specific models """
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

class ProductImage(Base):
    """ Attributes for the ProductImage model. Custom MapperExtension declarative
        for before insert and update methods. The migrate.versioning api does
        not handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'product_images'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('product_image_id', Integer(unsigned=True), primary_key=True)
    url = Column(String(2083), nullable=False)
    product_id = Column('product_id', Integer(unsigned=True),
        ForeignKey('products.product_id', name='fk_product_images_product_id',
        ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, url, product):
        self.url = url
        self.product = product

    #def __repr__(self):
        #return '<User %r>' % (self.name)

