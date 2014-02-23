"""
    video_sources models tests
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
from inspired.v1.lib.video_sources.models import VideoSource
from inspired.v1.lib.videos.models import Video

class TestVideoSourceModel(unittest.TestCase):
    """ test the video_sources model """

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
        cls.video = Video(name='abc')

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


    #@mock.patch('inspired.v1.lib.videos.models.Video')
    #def test_create_and_delete_video_source(self, video):
        #""" test creating and deleting a video_source """
        #video.return_value = Video
    def test_create_video_source(self):
        """ test creating a video_source """
        args = {
            'name': 'abc',
            'url': 'http://123.com',
            'source_id': '123', 
            'video': self.video,
        }
        video_source = VideoSource(**args)
        self.db_session.add(video_source)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_and_delete_video_source(self):
        args = {
            'name': 'abc',
            'url': 'http://123.com',
            'source_id': '123', 
            'video': self.video
        }
        video_source = VideoSource(**args)
        self.db_session.add(video_source)
        self.db_session.commit()
        self.db_session.delete(video_source)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_video_source_with_wrong_attribute(self):
        """ test creating a video_source with wrong attribute """
        args = {
            'name': 'abc',
            'url': 'http://123.com',
            'source_id': '123', 
            'video': self.video,
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: VideoSource(**args))
        self.db_session.commit()
        

    def test_query_all_one_video_source(self):
        """ test querying a video_source """
        args = {
            'name': 'abc',
            'url': 'http://123.com',
            'source_id': '123', 
            'video': self.video,
        }
        video_source = VideoSource(**args)
        self.db_session.add(video_source)
        self.db_session.commit()
        video_sources = [video_source]
        self.assertEqual([video_source], self.db_session.query(
            VideoSource).all())
        

    def test_query_all_two_video_sources(self):
        """ test querying two video_sources """
        args = {
            'name': 'abc1',
            'url': 'http://123.com',
            'source_id': '123', 
            'video': self.video,
        }
        video_source1 = VideoSource(**args)
        args = {
            'name': 'abc2',
            'url': 'http://1234.com',
            'source_id': '123', 
            'video': self.video,
        }
        video_source2 = VideoSource(**args)
        self.db_session.add(video_source1)
        self.db_session.add(video_source2)
        self.db_session.commit()
        self.assertEqual([video_source1, video_source2], 
            self.db_session.query(VideoSource).all())


if __name__ == '__main__':
    unittest.main()
        
