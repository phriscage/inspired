"""
    product_images models tests
"""
import os
import sys
import unittest
import mock
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../lib/'))
sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../conf/'))
sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../tests/lib_tests/'))
sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../../'))

from inspired_config import SQLALCHEMY_DATABASE_URI
TEST_URI = SQLALCHEMY_DATABASE_URI + '_test'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

from database import Base, init_engine, db_session, init_models
from inspired.v1.lib.product_images.models import ProductImage
from inspired.v1.lib.products.models import Product
from inspired.v1.lib.ref_product_types.models import RefProductType
from inspired.v1.lib.ref_product_styles.models import RefProductStyle

class TestProductImageModel(unittest.TestCase):
    """ test the product_images model """

    @classmethod
    def setUpClass(cls):
        """ Bootstrap test environment by creating the db engine
            we can mock the other sqlalchemy models or just create them below
         """
        cls.engine = init_engine(TEST_URI)
        cls.connection = cls.engine.connect()
        cls.db_session = db_session
        #cls.db_session = scoped_session(sessionmaker(autocommit=False,
                                         #autoflush=False,
                                         #bind=cls.engine))
        Base.query = cls.db_session.query_property()
        init_models()
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Delete the test schema and connection """
        Base.metadata.drop_all(cls.engine)
        cls.db_session.close()

    def setUp(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.begin(subtransactions=True)
        self.product = Product(upc=123, brand='abc', model='abc',
            product_type=RefProductType(name='abc'),
            product_style=RefProductStyle(name='abc'))

    def tearDown(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.rollback()
        self.db_session.close()
        self.engine.dispose()


    #@mock.patch('inspired.v1.lib.products.models.Product')
    #def test_create_and_delete_product_image(self, product):
        #""" test creating and deleting a product_image """
        #product.return_value = Product
    def test_create_product_image(self):
        """ test creating a product_image """
        args = {
            'url': 'http://123.com',
            'product': self.product,
        }
        product_image = ProductImage(**args)
        self.db_session.add(product_image)
        self.assertEqual(self.db_session.flush(), None)
        

    def test_create_and_delete_product_image(self):
        args = {
            'url': 'http://123.com',
            'product': self.product
        }
        product_image = ProductImage(**args)
        self.db_session.add(product_image)
        self.assertEqual(self.db_session.flush(), None)
        self.db_session.delete(product_image)
        self.assertEqual(self.db_session.flush(), None)
        

    def test_create_product_image_with_wrong_attribute(self):
        """ test creating a product_image with wrong attribute """
        args = {
            'url': 'http://123.com',
            'product': self.product,
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: ProductImage(**args))
        

    def test_create_two_product_images_same_url(self):
        """ test creating two product_images with the same url """
        args = {
            'url': 'http://123.com',
            'product': self.product,
        }
        product_image = ProductImage(**args)
        self.db_session.add(product_image)
        self.db_session.flush()
        args = {
            'url': 'http://123.com',
            'product': self.product,
        }
        product_image = ProductImage(**args)
        self.db_session.add(product_image)
        self.assertEqual(self.db_session.flush(), None)
        

    def test_query_all_one_product_image(self):
        """ test querying a product_image """
        args = {
            'url': 'http://123.com',
            'product': self.product,
        }
        product_image = ProductImage(**args)
        self.db_session.add(product_image)
        self.db_session.flush()
        product_images = [product_image]
        self.assertEqual([product_image], self.db_session.query(
            ProductImage).all())
        

    def test_query_all_two_product_images(self):
        """ test querying two product_images """
        args = {
            'url': 'http://123.com',
            'product': self.product,
        }
        product_image1 = ProductImage(**args)
        args = {
            'url': 'http://1234.com',
            'product': self.product,
        }
        product_image2 = ProductImage(**args)
        self.db_session.add(product_image1)
        self.db_session.add(product_image2)
        self.db_session.flush()
        self.assertEqual([product_image1, product_image2], 
            self.db_session.query(ProductImage).all())


if __name__ == '__main__':
    unittest.main()
        
