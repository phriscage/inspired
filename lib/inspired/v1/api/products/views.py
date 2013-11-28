"""
    views file contains all the routes for the products Blueprint and maps them
    to a specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import db_session
## need to import all child models for now
from inspired.v1.lib.products.models import Product
from inspired.v1.api.util import crossdomain
from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, jsonify, request, abort, make_response
from inspired.v1.helpers.serializers import JSONEncoder
import json

products = Blueprint('products', __name__)

#create routes
@products.route('/', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers='Content-Type')
#@requires_api_key
def post():
    """Create a new product.

    **Example request:**

    .. sourcecode:: http

       POST /products/create HTTP/1.1
       Accept: application/json
        data = {
            'email_address': 'abc.com',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }

    **Example response:**

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json
        data: {'id': <product id> }


    :statuscode 201: Created
    :statuscode 400: Bad Request
    :statuscode 409: Conflict
    """
    if not request.json:
        abort(400)
    for var in ['name', 'upc', 'ref_product_type_id', 'ref_product_style_id']:
        if var not in request.json:
            abort(400)
    try:
        product = Product.query.filter(Product.upc==request.json['upc']).one()
        return jsonify(message='Conflict', success=True), 409
    except NoResultFound as error:
        pass
    product = Product(**request.json)
    db_session.add(product)
    db_session.commit()
    message = 'Created: %s' % product.upc
    data = dict(id=product.id, upc=upc)
    return jsonify(message=message, data=data, success=True), 201
    

@products.route('/<int:product_id>', methods=['GET'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
#@requires_api_key
def get(product_id):
    """Get a product identified by `product_id`.

    **Example request:**

    .. sourcecode:: http

       GET /products/123 HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

        data = {
            'name': 'abc',
            'upc': '123'
            ...
        }

    :statuscode 200: success
    :statuscode 404: product does not exist
    """
    try:
        message = 'success'
        data = Product.query.filter(Product.id==product_id).first()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "'%s' record does not exist." % product_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        data = data.to_json
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=JSONEncoder))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response
