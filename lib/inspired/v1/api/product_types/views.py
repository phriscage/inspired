"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import db_session
from inspired.v1.lib.ref_product_types.models import RefProductType
from inspired.v1.api.util import crossdomain
from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, jsonify, request, abort, make_response
from inspired.v1.helpers.lazy_view import LazyView
from inspired.v1.helpers.serializers import JSONEncoder
import json

product_types = Blueprint('product_types', __name__)

#create routes
@product_types.route('', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers='Content-Type')
#@requires_api_key
def post():
    """Create a new product_type.

    **Example request:**

    .. sourcecode:: http

       POST /product_types HTTP/1.1
       Accept: application/json
        data = {
            'name': 'abc',
        }

    **Example response:**

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json
        data: {'id': <product_type id> }


    :statuscode 201: Created
    :statuscode 400: Bad Request
    :statuscode 409: Conflict
    """
    if not request.json or 'name' not in request.json:
        abort(400)
    try:
        product_type = RefProductType.query.filter(
            RefProductType.name==request.json['name']).one()
        return jsonify(message='Conflict', success=False), 409
    except NoResultFound as error:
        pass
    product_type = RefProductType(**request.json) 
    db_session.add(product_type)
    db_session.commit()
    message = 'Created: %s' % product_type.name
    data = dict(id=product_type.id, name=product_type.name)
    return jsonify(message=message, data=data, success=True), 201


@product_types.route('', methods=['GET'])
#@requires_api_key
def get_all():
    """Get all the product_types.

    **Example request:**

    .. sourcecode:: http

       GET /product_types HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
         "data": [
            {
                "id": 2,
                "name": "jeans",
            },
            {
                "id": 1,
                "name": "shirt",
            }
         ]
       }

    :statuscode 200: success
    :statuscode 404: product_types do not exist
    """
    columns = ['id', 'name']
    ## sqlalchemy query requires a column obj
    column_objs = [getattr(RefProductType, col) for col in columns]
    try:
        message = 'success'
        ## _asdict() is not available until sqlalchemy >= 0.8.0
        #data = [col._asdict() for col in
            #RefProductType.query.with_entities(*columns)]
        data = [dict([(key,value.__dict__[key]) for key in columns])
            for value in RefProductType.query.with_entities(*column_objs)]
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "No product_types data exists."
        return jsonify(error=404, message=message, success=False), 404
    else:
        #return json.dumps(data=data, message=message, success=True)
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)


@product_types.route('/<int:product_type_id>', methods=['GET'])
#@requires_api_key
def get(product_type_id):
    """Get a product_type identified by `product_type_id`.

    **Example request:**

    .. sourcecode:: http

       GET /product_types/123 HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
         "data": {
            "id": 123,
            "name": "tie",
            }
       }

    :statuscode 200: success
    :statuscode 404: product_type does not exist
    """
    columns = ['id', 'name']
    ## sqlalchemy query requires a column obj
    column_objs = [getattr(RefProductType, col) for col in columns]
    try:
        message = 'success'
        data = RefProductType.query.with_entities(*column_objs).filter(
            RefProductType.id==product_type_id).first()
        data = dict([(key,data.__dict__[key]) for key in columns])
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        #data = data.to_json
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=JSONEncoder))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response
