"""
    products models tests
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
from inspired.v1.lib.products.models import Product
from inspired.v1.lib.ref_product_types.models import RefProductType
from inspired.v1.lib.ref_product_styles.models import RefProductStyle

class TestProductModel(unittest.TestCase):
    """ test the products model """

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
        cls.product_type = RefProductType(name='abc')
        cls.product_style = RefProductStyle(name='abc')

    @classmethod
    def tearDownClass(cls):
        """Delete the test schema and connection """
        Base.metadata.drop_all(cls.engine)
        cls.db_session.close()

    def setUp(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.begin(subtransactions=True)

    def tearDown(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.rollback()
        self.db_session.close()
        self.engine.dispose()


    #@mock.patch('inspired.v1.lib.ref_product_types.models.RefProductType')
    #def test_create_and_delete_product(self, product_type):
        #""" test creating and deleting a product """
        #product_type.return_value = RefProductType
    def test_create_product(self):
        """ test creating a product """
        args = {
            'name': 'abc',
            'upc': '123',
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product = Product(**args)
        self.db_session.add(product)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_and_delete_product(self):
        args = {
            'name': 'abc',
            'upc': '123',
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product = Product(**args)
        self.db_session.add(product)
        self.db_session.commit()
        self.db_session.delete(product)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_product_with_wrong_attribute(self):
        """ test creating a product with wrong attribute """
        args = {
            'name': 'abc',
            'upc': '123',
            'product_type': self.product_type,
            'product_style': self.product_style,
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: Product(**args))
        self.db_session.commit()
        

    def test_create_two_products_same_name(self):
        """ test creating two products with the same name """
        args = {
            'name': 'abc',
            'upc': '123',
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product = Product(**args)
        self.db_session.add(product)
        self.db_session.commit()
        args = {
            'name': 'abc',
            'upc': '123',
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product = Product(**args)
        self.db_session.add(product)
        self.assertRaises(IntegrityError, lambda: self.db_session.commit())
        

    def test_query_all_one_product(self):
        """ test querying a product """
        args = {
            'name': 'abc',
            'upc': '123',
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product = Product(**args)
        self.db_session.add(product)
        self.db_session.commit()
        products = [product]
        self.assertEqual([product], self.db_session.query(
            Product).all())
        

    def test_query_all_two_products(self):
        """ test querying two products """
        args = {
            'name': 'abc1',
            'upc': '123',
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product1 = Product(**args)
        args = {
            'name': 'abc2',
            'upc': '1234',
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product2 = Product(**args)
        self.db_session.add(product1)
        self.db_session.add(product2)
        self.db_session.commit()
        self.assertEqual([product1, product2], 
            self.db_session.query(Product).all())


if __name__ == '__main__':
    unittest.main()
        
