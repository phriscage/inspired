"""
    artists models tests
"""
import os
import sys
import unittest
import mock

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
from inspired.v1.lib.artists.models import Artist, artist_videos
from inspired.v1.lib.videos.models import Video

class TestArtistModel(unittest.TestCase):
    """ test the artists model """

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


    def test_create_artist(self):
        """ test creating a artist """
        args = {
            'name': 'abc',
            'first_name': 'abc',
            'last_name': 'abc',
        }
        artist = Artist(**args)
        self.db_session.add(artist)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_artist_with_video(self):
        """ test creating a artist with video """
        args = {
            'name': 'abc',
            'first_name': 'abc',
            'last_name': 'abc',
            'videos': [self.video]
        }
        artist = Artist(**args)
        self.db_session.add(artist)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_and_delete_artist(self):
        args = {
            'name': 'abc',
            'first_name': 'abc',
            'last_name': 'abc',
        }
        artist = Artist(**args)
        self.db_session.add(artist)
        self.db_session.commit()
        self.db_session.delete(artist)
        self.assertEqual(self.db_session.commit(), None)
        

    def test_create_artist_with_wrong_attribute(self):
        """ test creating a artist with wrong attribute """
        args = {
            'name': 'abc',
            'first_name': 'abc',
            'last_name': 'abc',
            'asdfas': 'asdfs'
        }
        self.assertRaises(TypeError, lambda: Artist(**args))
        self.db_session.commit()
        

    def test_create_two_artists_same_name(self):
        """ test creating two artists with the same name """
        args = {
            'name': 'abc',
            'first_name': 'abc',
            'last_name': 'abc',
        }
        artist = Artist(**args)
        self.db_session.add(artist)
        self.db_session.commit()
        args = {
            'name': 'abc',
            'first_name': 'abc',
            'last_name': 'abc',
        }
        artist = Artist(**args)
        self.db_session.add(artist)
        self.assertRaises(IntegrityError, lambda: self.db_session.commit())
        

    def test_query_all_one_artist(self):
        """ test querying a artist """
        args = {
            'name': 'abc',
            'first_name': 'abc',
            'last_name': 'abc',
        }
        artist = Artist(**args)
        self.db_session.add(artist)
        self.db_session.commit()
        artists = [artist]
        self.assertEqual([artist], self.db_session.query(
            Artist).all())
        

    def test_query_all_two_artists(self):
        """ test querying two artists """
        args = {
            'name': 'abc1',
            'first_name': 'abc',
            'last_name': 'abc',
        }
        artist1 = Artist(**args)
        args = {
            'name': 'abc2',
            'first_name': 'abcd',
            'last_name': 'abc',
        }
        artist2 = Artist(**args)
        self.db_session.add(artist1)
        self.db_session.add(artist2)
        self.db_session.commit()
        self.assertEqual([artist1, artist2], 
            self.db_session.query(Artist).all())


if __name__ == '__main__':
    unittest.main()
        
