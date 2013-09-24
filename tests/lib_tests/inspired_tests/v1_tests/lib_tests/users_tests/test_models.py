"""
    user models tests
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
from inspired.v1.lib.users.models import User

class TestUserModel(unittest.TestCase):
    """ test the user model """

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


    def test_create_user(self):
        """ test creating a user """
        args = {
            'email_address': 'abc.com',
            'password': 'abc',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user = User(**args)
        self.db_session.add(user)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_and_delete_user(self):
        """ test creating and deleting a user """
        args = {
            'email_address': 'abc.com',
            'password': 'abc',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user = User(**args)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.delete(user)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_user_with_wrong_attribute(self):
        """ test creating a user with wrong attribute """
        args = {
            'email_address': 'abc.com',
            'password': 'abc',
            'first_name': 'Joe',
            'last_name': 'Schome',
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: User(**args))
        self.db_session.commit()
        

    def test_create_two_users_same_email_address(self):
        """ test creating two users with the same email address """
        args = {
            'email_address': 'abc.com',
            'password': 'abc',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user = User(**args)
        self.db_session.add(user)
        self.db_session.commit()
        args = {
            'email_address': 'abc.com',
            'password': 'abc',
            'first_name': 'Bill',
            'last_name': 'Smith'
        }
        user = User(**args)
        self.db_session.add(user)
        self.assertRaises(IntegrityError, lambda: self.db_session.commit())
        

    def test_query_all_one_user(self):
        """ test querying a user """
        args = {
            'email_address': 'abc.com',
            'password': 'abc',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user = User(**args)
        self.db_session.add(user)
        self.db_session.commit()
        users = [user]
        self.assertEqual([user], self.db_session.query(User).all())
        

    def test_query_all_two_users(self):
        """ test querying two users """
        args = {
            'email_address': 'abc.com',
            'password': 'abc',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user1 = User(**args)
        args = {
            'email_address': 'abc1.com',
            'password': 'abc',
            'first_name': 'Bill',
            'last_name': 'Smith'
        }
        user2 = User(**args)
        self.db_session.add(user1)
        self.db_session.add(user2)
        self.db_session.commit()
        self.assertEqual([user1, user2], self.db_session.query(User).all())


if __name__ == '__main__':
    unittest.main()
        
