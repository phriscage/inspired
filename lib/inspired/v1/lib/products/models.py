""" the products.models file contains the all the specific models """
from __future__ import absolute_import
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../../../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import Base
from inspired.v1.lib.helpers import BaseExtension
#from product_sources.models import ProductSource
#from scenes.models import Scene
from sqlalchemy import Column, String, DateTime, Table, ForeignKey, Text
from sqlalchemy.dialects.mysql import INTEGER as Integer, DECIMAL as Decimal
from sqlalchemy.orm import relationship, backref

class Product(Base):
    """ Attributes for the Product model. Custom MapperExtension declarative for
        before insert and update methods. The migrate.versioning api does not
        handle sqlalchemy.dialects.mysql for custom column attributes. I.E.
        INTEGER(unsigned=True), so they need to be modified manually.
     """
    __tablename__ = 'products'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    ## mapper extension declarative for before insert and before update
    __mapper_args__ = { 'extension': BaseExtension() }

    id = Column('product_id', Integer(unsigned=True), primary_key=True)
    upc = Column(Decimal(12,0), unique=True, index=True, nullable=False)
    brand = Column(String(120), nullable=False)
    model = Column(String(120), nullable=False)
    description = Column(Text())
    product_images = relationship("ProductImage", backref="product")
    ref_product_type_id = Column('ref_product_type_id', Integer(4, 
        unsigned=True), ForeignKey('ref_product_types.ref_product_type_id',
        name='fk_products_ref_product_type_id', ondelete="CASCADE"), 
        nullable=False, index=True)
    product_type = relationship("RefProductType", backref="products")
    ref_product_style_id = Column('ref_product_style_id', Integer(4, 
        unsigned=True), ForeignKey('ref_product_styles.ref_product_style_id',
        name='fk_products_ref_product_style_id', ondelete="CASCADE"), 
        nullable=False, index=True)
    product_style = relationship("RefProductStyle", backref="products")
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def __init__(self, upc, brand, model, description, product_type,
        product_style, ref_product_type_id=None, ref_product_style_id=None):
        self.upc = upc
        self.brand = brand
        self.model = model
        self.description = description
        self.product_type = product_type
        self.product_style = product_style
        self.ref_product_type_id = ref_product_type_id
        self.ref_product_style_id = ref_product_style_id

    #def __repr__(self):
        #return '<User %r>' % (self.name)

