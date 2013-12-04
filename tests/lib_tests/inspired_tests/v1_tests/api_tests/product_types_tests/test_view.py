""" 
    product_types.view test
"""

import json
import os
import sys
import unittest
#import mock

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
from inspired.v1.lib.ref_product_types.models import RefProductType
from inspired.v1.api.main import  create_app

class ProductsApiTestCase(unittest.TestCase):
    """Tests for the API /v1/products methods"""

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
        ## need to clear the table and auto-increment counter
        self.connection.execute("TRUNCATE ref_product_types")
        self._ctx.pop()  


    def test_check_if_product_type_exists(self):
        """ testing checking if a product_type exists """
        name = 'abc'
        args = {
            'name': name,
        }
        product_type = RefProductType(**args)
        self.db_session.add(product_type)
        self.db_session.commit()
        response = self.client.get('/api/v1/product_types/%i' % product_type.id)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertTrue(json.loads(response.data)['success'])
        for var in ['name']:
            self.assertEquals(json.loads(response.data)['data'][var], 
                locals()[var])
        self.db_session.delete(product_type)
        self.assertEqual(self.db_session.commit(), None)


    def test_add_one_product_type(self):
        """ testing adding a product_type """
        name = 'abc'
        args = {
            'name': name,
        }
        response = self.client.post('/api/v1/product_types', data=json.dumps(args),
            content_type='application/json')
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertEquals(response.status_code, 201)
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEquals(json.loads(response.data)['data']['id'], 1)


    def test_add_two_product_types(self):
        """ testing adding two product_types """
        name = 'abc'
        args = {
            'name': name,
        }
        name = 'xyz'
        args2 = {
            'name': name,
        }
        for id, values in enumerate([args, args2], 1):
            response = self.client.post('/api/v1/product_types', 
                data=json.dumps(values), 
                content_type='application/json')
            self.assertEquals(response.headers['Content-Type'], 
                'application/json')
            self.assertEquals(response.status_code, 201)
            self.assertTrue(json.loads(response.data)['success'])
            self.assertEquals(json.loads(response.data)['data']['id'], id)


    def test_add_two_product_types_same_name(self):
        """ testing adding two product_types with same name """
        name = 'abc'
        args = {
            'name': name,
        }
        args2 = {
            'name': name,
        }
        for id, values in enumerate([args, args2], 1):
            response = self.client.post('/api/v1/product_types', 
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
