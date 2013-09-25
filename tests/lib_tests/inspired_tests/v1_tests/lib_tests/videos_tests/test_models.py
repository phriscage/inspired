"""
    video models tests
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
from inspired.v1.lib.videos.models import Video

class TestVideoModel(unittest.TestCase):
    """ test the video model """

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

    def tearDown(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.rollback()
        self.db_session.close()
        self.engine.dispose()


    def test_create_video(self):
        """ test creating a video """
        args = {
            'name': 'abc',
        }
        video = Video(**args)
        self.db_session.add(video)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_and_delete_video(self):
        """ test creating and deleting a video """
        args = {
            'name': 'abc',
        }
        video = Video(**args)
        self.db_session.add(video)
        self.db_session.commit()
        self.db_session.delete(video)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_video_with_wrong_attribute(self):
        """ test creating a video with wrong attribute """
        args = {
            'name': 'abc',
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: Video(**args))
        self.db_session.commit()
        

    def test_create_two_videos_same_name(self):
        """ test creating two videos with the same name """
        args = {
            'name': 'abc',
        }
        video = Video(**args)
        self.db_session.add(video)
        self.db_session.commit()
        args = {
            'name': 'abc',
        }
        video = Video(**args)
        self.db_session.add(video)
        self.assertRaises(IntegrityError, lambda: self.db_session.commit())
        

    def test_query_all_one_video(self):
        """ test querying a video """
        args = {
            'name': 'abc',
        }
        video = Video(**args)
        self.db_session.add(video)
        self.db_session.commit()
        videos = [video]
        self.assertEqual([video], self.db_session.query(Video).all())
        

    def test_query_all_two_videos(self):
        """ test querying two videos """
        args = {
            'name': 'abc1',
        }
        video1 = Video(**args)
        args = {
            'name': 'abc2',
        }
        video2 = Video(**args)
        self.db_session.add(video1)
        self.db_session.add(video2)
        self.db_session.commit()
        self.assertEqual([video1, video2], self.db_session.query(Video).all())


if __name__ == '__main__':
    unittest.main()
        
