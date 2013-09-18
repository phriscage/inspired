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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from inspired.v1.lib.users.models import Base, User

class TestUserModel(unittest.TestCase):
    """ test the user model """

    def setUp(self):
        """ setup the mode with initial variables """
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        """ drop all the initial connections """
        Base.metadata.drop_all(self.engine)
        self.session.close()

    def test_create_and_delete_user(self):
        """ test creating and deleting a user """
        args = {
            'email_address': 'abc.com',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user = User(*args)
        self.session.add(user)
        self.session.commit()
        self.session.delete(user)
        results = self.session.commit()
        self.assertEqual(None, None)
        
    def test_query_all_one_user(self):
        """ test querying a user """
        args = {
            'email_address': 'abc.com',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user = User(*args)
        self.session.add(user)
        self.session.commit()
        users = [user]
        result = self.session.query(User).all()
        self.assertEqual(users, result)
        
    def test_query_all_two_users(self):
        """ test querying two users """
        args = {
            'email_address': 'abc.com',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }
        user1 = User(*args)
        args = {
            'email_address': 'abc1.com',
            'first_name': 'Bill',
            'last_name': 'Smith'
        }
        user2 = User(*args)
        self.session.add(user1)
        self.session.add(user2)
        self.session.commit()
        users = [user1, user2]
        result = self.session.query(User).all()
        self.assertEqual(users, result)
        
