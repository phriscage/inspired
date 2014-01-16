""" the product_retailers.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
#from product_retailer_sources.models import RetailerSource
#from scenes.models import Scene
from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer, DECIMAL as Decimal
from sqlalchemy.orm import relationship, backref

class ProductRetailer(Base):
    """ Attributes for the ProductRetailer model. Custom MapperExtension 
        declarative for before insert and update methods. The migrate.versioning
        api does not handle sqlalchemy.dialects.mysql for custom column 
        attributes. I.E. INTEGER(unsigned=True), so they need to be modified 
        manually.
     """
    __tablename__ = 'product_retailers'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('product_retailer_id', Integer(unsigned=True), primary_key=True)
    url = Column(String(255), nullable=False)
    price = Column(Decimal(10,2))
    product_id = Column('product_id', Integer(unsigned=True), 
        ForeignKey('products.product_id', name='fk_product_retailers_product_id',
        ondelete="CASCADE"), nullable=False, index=True)
    #product = relationship("Product", backref="product_retailers")
    retailer_id = Column('retailer_id', Integer(unsigned=True),
        ForeignKey('retailers.retailer_id', name='fk_product_retailers_retailer_id',
        ondelete="CASCADE"), nullable=False, index=True)
    retailer = relationship("Retailer", backref="product_retailers")
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, url, product, retailer, price=None, product_id=None, 
        retailer_id=None):
        self.url = url
        self.product = product
        self.retailer = retailer
        self.price = price
        self.product_id = product_id
        self.retailer_id = retailer_id

    #def __repr__(self):
        #return '<User %r>' % (self.name)

