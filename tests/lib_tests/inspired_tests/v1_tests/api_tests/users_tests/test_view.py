""" 
    users.view test
"""

import json
#import mock
import os
import sys
import unittest
import mock
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../../'))
sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../lib/'))
sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../conf/'))

#from inspired_config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, init_engine, db_session
from inspired.v1.lib.users.models import User
from lib.main import  create_app

class UsersApiTestCase(unittest.TestCase):
    """Tests for the API /v1/users methods"""

    @classmethod
    def setUpClass(cls):
        """Bootstrap test environment by creating the db engine and app """
        cls.app = create_app('sqlite:///:memory:')
        cls.app.config['TESTING'] = True
        cls.app.config['CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()
        #cls.engine = create_engine('sqlite:///:memory:',
                    #connect_args={'check_same_thread':False},
                    #poolclass=StaticPool)
        cls._ctx = cls.app.test_request_context()
        cls._ctx.push()
        cls.engine = create_engine('sqlite:///:memory:')
        cls.session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=cls.engine))
        Base.query = cls.session.query_property()
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Delete the test schema and connection """
        #cls.patcher.stop()
        Base.metadata.drop_all(cls.engine)
        cls.session.close()

    def setUp(self):
        """ use subsessions and do a rollback after each test. """
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        self.session.begin(subtransactions=True)

    def tearDown(self):
        """ use subsessions and do a rollback after each test. """
        self.session.rollback()
        #self.session.close()
        self.engine.dispose()
        self._ctx.pop()  


    def test_check_if_user_exists(self):
        """ testing checking if a user exists """
        email_address = 'abc.com'
        first_name = 'Joe'
        last_name = 'Schome'
        args = {
            'email_address': email_address,
            'first_name': first_name,
            'last_name': last_name
        }
        user = User(**args)
        self.session.add(user)
        self.session.commit()
        response = self.client.get('/api/v1/users/%i' % user.id)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertTrue(json.loads(response.data)['success'])
        for var in ['email_address', 'first_name', 'last_name']:
            self.assertEquals(json.loads(response.data)['data'][var], 
                locals()[var])
        self.session.delete(user)
        self.assertEqual(self.session.commit(), None)


    #@mock.patch('database.db_session')
    #def test_add_one_user(self, db_session):
    def test_add_one_user(self):
        """ testing adding a user """
        email_address = 'abc.com'
        first_name = 'Joe'
        last_name = 'Schome'
        args = {
            'email_address': email_address,
            'first_name': first_name,
            'last_name': last_name
        }
        #user = User(**args)
        #self.session.add(user)
        #self.session.commit()
        response = self.client.post('/api/v1/users/', data=json.dumps(args), 
            content_type='application/json')
        print response.data
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertTrue(json.loads(response.data)['success'])
        response = self.client.get('/api/v1/users/1')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertTrue(json.loads(response.data)['success'])
        for var in ['email_address', 'first_name', 'last_name']:
            self.assertEquals(json.loads(response.data)['data'][var], 
                locals()[var])
        self.session.delete(user)
        self.assertEqual(self.session.commit(), None)



if __name__ == "__main__":
    unittest.main()
