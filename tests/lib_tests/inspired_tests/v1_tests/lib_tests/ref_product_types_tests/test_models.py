"""
    ref_product_type models tests
"""
import os
import sys
import unittest
#import mock
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
from inspired.v1.lib.ref_product_types.models import RefProductType

class TestRefProductTypeModel(unittest.TestCase):
    """ test the ref_product_type model """

    @classmethod
    def setUpClass(cls):
        """Bootstrap test environment by creating the db engine """
        cls.engine = init_engine(TEST_URI)
        cls.connection = cls.engine.connect()
        cls.db_session = db_session
        #cls.db_session = scoped_session(sessionmaker(autocommit=False,
                                         #autoflush=False,
                                         #bind=cls.engine))
        Base.query = cls.db_session.query_property()
        Base.metadata.create_all(cls.engine)

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


    def test_create_ref_product_type(self):
        """ test creating a ref_product_type """
        args = {
            'name': 'abc',
        }
        ref_product_type = RefProductType(**args)
        self.db_session.add(ref_product_type)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_and_delete_ref_product_type(self):
        """ test creating and deleting a ref_product_type """
        args = {
            'name': 'abc',
        }
        ref_product_type = RefProductType(**args)
        self.db_session.add(ref_product_type)
        self.db_session.commit()
        self.db_session.delete(ref_product_type)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_ref_product_type_with_wrong_attribute(self):
        """ test creating a ref_product_type with wrong attribute """
        args = {
            'name': 'abc',
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: RefProductType(**args))
        self.db_session.commit()
        

    def test_create_two_ref_product_types_same_name(self):
        """ test creating two ref_product_types with the same name """
        args = {
            'name': 'abc',
        }
        ref_product_type = RefProductType(**args)
        self.db_session.add(ref_product_type)
        self.db_session.commit()
        args = {
            'name': 'abc',
        }
        ref_product_type = RefProductType(**args)
        self.db_session.add(ref_product_type)
        self.assertRaises(IntegrityError, lambda: self.db_session.commit())
        

    def test_query_all_one_ref_product_type(self):
        """ test querying a ref_product_type """
        args = {
            'name': 'abc',
        }
        ref_product_type = RefProductType(**args)
        self.db_session.add(ref_product_type)
        self.db_session.commit()
        ref_product_types = [ref_product_type]
        self.assertEqual([ref_product_type],
            self.db_session.query(RefProductType).all())
        

    def test_query_all_two_ref_product_types(self):
        """ test querying two ref_product_types """
        args = {
            'name': 'abc',
        }
        ref_product_type1 = RefProductType(**args)
        args = {
            'name': 'abc1',
        }
        ref_product_type2 = RefProductType(**args)
        self.db_session.add(ref_product_type1)
        self.db_session.add(ref_product_type2)
        self.db_session.commit()
        self.assertEqual([ref_product_type1, ref_product_type2], 
            self.db_session.query(RefProductType).all())


if __name__ == '__main__':
    unittest.main()
        
