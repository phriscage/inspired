""" 
    products.view test
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
from inspired.v1.lib.products.models import Product
from inspired.v1.lib.ref_product_types.models import RefProductType
from inspired.v1.lib.ref_product_styles.models import RefProductStyle
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
        self.product_type = RefProductType(name='abc')
        self.product_style = RefProductStyle(name='abc')
        self.db_session.add(self.product_type)
        self.db_session.add(self.product_style)
        self.db_session.commit()

    def tearDown(self):
        """ use subsessions and do a rollback after each test. """
        self.db_session.rollback()
        self.db_session.close()
        self.engine.dispose()
        ## need to clear the table and auto-increment counter
        self.connection.execute("TRUNCATE products")
        self.connection.execute("TRUNCATE ref_product_types")
        self.connection.execute("TRUNCATE ref_product_styles")
        self._ctx.pop()  


    def test_check_if_product_exists(self):
        """ testing checking if a product exists """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': self.product_type,
            'product_style': self.product_style,
        }
        product = Product(**args)
        self.db_session.add(product)
        self.db_session.commit()
        response = self.client.get('/api/v1/products/%i' % product.id)
        #print response.data
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertTrue(json.loads(response.data)['success'])
        for var in ['upc', 'brand', 'model']:
            self.assertEquals(json.loads(response.data)['data'][var], 
                locals()[var])
        self.db_session.delete(product)
        self.assertEqual(self.db_session.commit(), None)


    def test_add_one_product(self):
        """ testing adding a product """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': self.product_type.id,
            },
            'product_style': {
                'id': self.product_style.id,
            },
            'product_images': [{
                'url': 'http://abc.com/abc.png'
            }, {
                'url': '/static/abc.png'
            }]
        }
        response = self.client.post('/api/v1/products', data=json.dumps(args),
            content_type='application/json')
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertEquals(response.status_code, 201)
        self.assertTrue(json.loads(response.data)['success'])
        self.assertEquals(json.loads(response.data)['data']['id'], 1)


    def test_add_one_product_with_out_product_type_attribute(self):
        """ testing adding a product with out product_type attribute """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_style': {
                'id': self.product_style.id,
            }
        }
        response = self.client.post('/api/v1/products', data=json.dumps(args),
            content_type='application/json')
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertEquals(response.status_code, 400)
        self.assertFalse(json.loads(response.data)['success'])
        self.assertEquals(json.loads(response.data)['message'], 
            "400: Bad Request")


    def test_add_one_product_with_out_product_style_attribute(self):
        """ testing adding a product with out product_style attribute """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': self.product_type.id,
            }
        }
        response = self.client.post('/api/v1/products', data=json.dumps(args),
            content_type='application/json')
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertEquals(response.status_code, 400)
        self.assertFalse(json.loads(response.data)['success'])
        self.assertEquals(json.loads(response.data)['message'], 
            "400: Bad Request")


    def test_add_one_product_with_missing_product_type(self):
        """ testing adding a product with missing product_type """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        id = 9999
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': id,
            },
            'product_style': {
                'id': self.product_style.id,
            },
            'product_images': [{
                'url': 'http://abc.com/abc.png'
            }, {
                'url': '/static/abc.png'
            }]
        }
        response = self.client.post('/api/v1/products', data=json.dumps(args),
            content_type='application/json')
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertEquals(response.status_code, 404)
        self.assertFalse(json.loads(response.data)['success'])
        self.assertEquals(json.loads(response.data)['message'], 
            "Product Type '%i' Not Found" % id)


    def test_add_one_product_with_missing_product_style(self):
        """ testing adding a product with missing product_style """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        id = 9999 
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': self.product_type.id,
            },
            'product_style': {
                'id': id
            },
            'product_images': [{
                'url': 'http://abc.com/abc.png'
            }, {
                'url': '/static/abc.png'
            }]
        }
        response = self.client.post('/api/v1/products', data=json.dumps(args),
            content_type='application/json')
        self.assertEquals(response.headers['Content-Type'], 'application/json')
        self.assertEquals(response.status_code, 404)
        self.assertFalse(json.loads(response.data)['success'])
        self.assertEquals(json.loads(response.data)['message'], 
            "Product Style '%i' Not Found" % id)


    def test_add_two_products(self):
        """ testing adding two products """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': self.product_type.id,
            },
            'product_style': {
                'id': self.product_style.id,
            },
            'product_images': [{
                'url': 'http://abc.com/abc.png'
            }, {
                'url': '/static/abc.png'
            }]
        }
        upc = '1234'
        brand = 'xyz'
        model = 'abc'
        args2 = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': self.product_type.id,
            },
            'product_style': {
                'id': self.product_style.id,
            },
            'product_images': [{
                'url': 'http://abc.com/abc.png'
            }, {
                'url': '/static/abc.png'
            }]
        }
        for id, values in enumerate([args, args2], 1):
            response = self.client.post('/api/v1/products', 
                data=json.dumps(values), 
                content_type='application/json')
            self.assertEquals(response.headers['Content-Type'], 
                'application/json')
            self.assertEquals(response.status_code, 201)
            self.assertTrue(json.loads(response.data)['success'])
            self.assertEquals(json.loads(response.data)['data']['id'], id)


    def test_add_two_products_same_upc(self):
        """ testing adding two products with same upc """
        upc = '123'
        brand = 'abc'
        model = 'abc'
        args = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': self.product_type.id,
            },
            'product_style': {
                'id': self.product_style.id,
            },
            'product_images': [{
                'url': 'http://abc.com/abc.png'
            }, {
                'url': '/static/abc.png'
            }]
        }
        upc = '123'
        brand = 'abc'
        model = 'abc'
        args2 = {
            'upc': upc,
            'brand': brand,
            'model': model,
            'product_type': {
                'id': self.product_type.id,
            },
            'product_style': {
                'id': self.product_style.id,
            },
            'product_images': [{
                'url': 'http://abc.com/abc.png'
            }, {
                'url': '/static/abc.png'
            }]
        }
        for id, values in enumerate([args, args2], 1):
            response = self.client.post('/api/v1/products', 
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
