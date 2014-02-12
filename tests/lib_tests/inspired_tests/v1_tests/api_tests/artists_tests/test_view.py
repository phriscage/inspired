""" 
    artists.view test
"""

import json
#import mock
import os
import sys
import unittest
import mock
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '../../../../../../../'))
sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../lib/'))
sys.path.insert(0, os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../../../conf/'))

from inspired_config import SQLALCHEMY_DATABASE_URI
TEST_URI = SQLALCHEMY_DATABASE_URI + '_test'

#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.pool import StaticPool

from database import Base, init_engine, db_session, init_models
from inspired.v1.lib.artists.models import Artist
from inspired.v1.lib.videos.models import Video
from inspired.v1.api.main import create_app

class ArtistsApiTestCase(unittest.TestCase):
    """Tests for the API /v1/artists methods"""

    @classmethod
    def setUpClass(cls):
        """Bootstrap test environment by creating the db engine and app """
        init_models()
        cls.app = create_app(TEST_URI)
        cls.app.config['TESTING'] = True
        cls.app.config['CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()
        #cls.engine = create_engine('sqlite:///:memory:',
                    #connect_args={'check_same_thread':False},
                    #poolclass=StaticPool)
        cls._ctx = cls.app.test_request_context()
        cls._ctx.push()
        cls.engine = init_engine(TEST_URI)
        cls.connection = cls.engine.connect()
        cls.db_session = db_session
        Base.query = cls.db_session.query_property()
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Delete the test schema and connection """
        Base.metadata.drop_all(cls.engine)
        cls.db_session.close()

    def setUp(self):
        """ use subsessions and do a rollback after each test. """
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        self.db_session.begin(subtransactions=True)
        self.video = Video(name='abc')
        self.db_session.add(self.video)
        self.db_session.commit()

    def tearDown(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.rollback()
        self.db_session.close()
        self.engine.dispose()
        ## need to clear the table and auto-increment counter
        self.connection.execute("TRUNCATE artists")
        self.connection.execute("TRUNCATE videos")
        self._ctx.pop()  


    def test_check_if_artist_exists(self):
        """ testing checking if a artist exists """
        name = "Abc"
        first_name = "A"
        last_name = "bc"
        args = {
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
        }
        artist = Artist(**args)
        self.db_session.add(artist)
        self.db_session.flush()
        response = self.client.get('/api/v1/artists/%i' % artist.id)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertTrue(json.loads(response.data)['success'])
        for var in ['name', 'first_name', 'last_name']:
            self.assertEquals(json.loads(response.data)['data'][var], 
                locals()[var])
        self.db_session.delete(artist)
        self.assertEqual(self.db_session.flush(), None)


    def test_add_one_artist(self):
        """ testing adding a artist """
        name = 'Abc'
        first_name = 'A'
        last_name = 'abc'
        args = {
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
            #'artist_images': [{
                #'url': 'http://abc.com/abc.png'
            #}, {
                #'url': '/static/abc.png'
            #}]
        }
        response = self.client.post('/api/v1/artists', data=json.dumps(args),
            content_type='application/json')
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertEquals(response.status_code, 201)
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEquals(json.loads(response.data)['data']['id'], 1)


    def test_add_two_artists(self):
        """ testing adding two artists """
        name = 'Abc'
        first_name = 'A'
        last_name = 'abc'
        args = {
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
        }
        name = 'Abcd'
        first_name = 'A'
        last_name = 'abc'
        args2 = {
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
        }
        for id, values in enumerate([args, args2], 1):
            response = self.client.post('/api/v1/artists', 
                data=json.dumps(values), 
                content_type='application/json')
            self.assertEquals(response.headers['Content-Type'], 
                'application/json')
            self.assertEquals(response.status_code, 201)
            self.assertTrue(json.loads(response.data)['success'])
            self.assertEquals(json.loads(response.data)['data']['id'], id)


    def test_add_two_artists_same_name(self):
        """ testing adding two artists with same name """
        name = 'Abc'
        first_name = 'A'
        last_name = 'abc'
        args = {
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
        }
        name = 'Abc'
        first_name = 'A'
        last_name = 'abc'
        args2 = {
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
        }
        for id, values in enumerate([args, args2], 1):
            response = self.client.post('/api/v1/artists', 
                data=json.dumps(values), 
                content_type='application/json')
            self.assertEquals(response.headers['Content-Type'], 
                'application/json')
            if id == 1:
                self.assertEquals(response.status_code, 201)
                self.assertEquals(json.loads(response.data)['data']['id'], id)
                self.assertTrue(json.loads(response.data)['success'])
            else:
                self.assertEquals(response.status_code, 409)
                self.assertFalse(json.loads(response.data)['success'])


if __name__ == "__main__":
    unittest.main()
