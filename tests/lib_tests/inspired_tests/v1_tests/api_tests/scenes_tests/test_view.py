""" 
    scenes.view test
"""

import json
#import mock
import os
import sys
import unittest
import mock
import sqlite3
import datetime

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
from inspired.v1.lib.scenes.models import Scene
from inspired.v1.lib.videos.models import Video
from inspired.v1.api.main import  create_app

class ScenesApiTestCase(unittest.TestCase):
    """Tests for the API /v1/scenes methods"""

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

    def tearDown(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.rollback()
        self.db_session.close()
        self.engine.dispose()
        self._ctx.pop()  

    def test_check_if_scene_exist(self):
        """ testing checking if scene exist """
        video = Video(name="Titanic")
        self.db_session.add(video)
        self.db_session.commit()
        name = "Scene 1"
        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        scene = Scene(name=name,start_time=start_time,end_time=end_time)
        scene.video_id, video_id = video.id, video.id
        self.db_session.add(scene)
        self.db_session.commit()    
        response = self.client.get('/api/v1/scene/%i' % scene.id)
        #print response
        self.assertEquals(response.status_code, 200)
        #self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertTrue(json.loads(response.data)['success'])
        for var in ['name',"video_id"]:
            self.assertEquals(str(json.loads(response.data)['data'][var]), str(locals()[var]))
        self.assertEquals(str(json.loads(response.data)['data']["start_time"]),str(start_time.isoformat())) 
        self.assertEquals(str(json.loads(response.data)['data']["end_time"]),str(end_time.isoformat())) 
        self.db_session.delete(video)
        self.db_session.delete(scene)
        self.assertEqual(self.db_session.commit(), None)

if __name__ == "__main__":
    unittest.main()
