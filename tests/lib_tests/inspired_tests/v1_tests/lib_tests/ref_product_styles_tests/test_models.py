"""
    ref_product_style models tests
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
from inspired.v1.lib.ref_product_styles.models import RefProductStyle

class TestRefProductStyleModel(unittest.TestCase):
    """ test the ref_product_style model """

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


    def test_create_ref_product_style(self):
        """ test creating a ref_product_style """
        args = {
            'name': 'abc',
        }
        ref_product_style = RefProductStyle(**args)
        self.db_session.add(ref_product_style)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_and_delete_ref_product_style(self):
        """ test creating and deleting a ref_product_style """
        args = {
            'name': 'abc',
        }
        ref_product_style = RefProductStyle(**args)
        self.db_session.add(ref_product_style)
        self.db_session.commit()
        self.db_session.delete(ref_product_style)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_ref_product_style_with_wrong_attribute(self):
        """ test creating a ref_product_style with wrong attribute """
        args = {
            'name': 'abc',
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: RefProductStyle(**args))
        self.db_session.commit()
        

    def test_create_two_ref_product_styles_same_name(self):
        """ test creating two ref_product_styles with the same name """
        args = {
            'name': 'abc',
        }
        ref_product_style = RefProductStyle(**args)
        self.db_session.add(ref_product_style)
        self.db_session.commit()
        args = {
            'name': 'abc',
        }
        ref_product_style = RefProductStyle(**args)
        self.db_session.add(ref_product_style)
        self.assertRaises(IntegrityError, lambda: self.db_session.commit())
        

    def test_query_all_one_ref_product_style(self):
        """ test querying a ref_product_style """
        args = {
            'name': 'abc',
        }
        ref_product_style = RefProductStyle(**args)
        self.db_session.add(ref_product_style)
        self.db_session.commit()
        ref_product_styles = [ref_product_style]
        self.assertEqual([ref_product_style],
            self.db_session.query(RefProductStyle).all())
        

    def test_query_all_two_ref_product_styles(self):
        """ test querying two ref_product_styles """
        args = {
            'name': 'abc',
        }
        ref_product_style1 = RefProductStyle(**args)
        args = {
            'name': 'abc1',
        }
        ref_product_style2 = RefProductStyle(**args)
        self.db_session.add(ref_product_style1)
        self.db_session.add(ref_product_style2)
        self.db_session.commit()
        self.assertEqual([ref_product_style1, ref_product_style2], 
            self.db_session.query(RefProductStyle).all())


if __name__ == '__main__':
    unittest.main()
        
