"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from inspired.v1.lib.ref_product_types.models import RefProductType

from flask import Blueprint, jsonify, request
from inspired.v1.helpers.lazy_view import LazyView
from inspired.v1.helpers.serializers import JSONEncoder
import json

product_types = Blueprint('product_types', __name__)

#create routes
@product_types.route('/', methods=['GET'])
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
             "name": "originial",
           },
           {
             "name": "low_end",
           }
         ]
       }

    :statuscode 200: success
    :statuscode 404: product_types do not exist
    """
    try:
        #data, message = ([{'name': 'abc'}, {'name': 'xyz'}], 'test message')
        message = 'success'
        data = [obj.to_json for obj in RefProductType.query.all()]
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
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
             "name": "originial",
            }
       }

    :statuscode 200: success
    :statuscode 404: product_type does not exist
    """
    try:
        message = 'success'
        data = RefProductType.query.filter(RefProductType.id==product_type_id).first()
        data = data.to_json
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        return jsonify(error=404, message=message, success=False), 404
    else:
        #return json.dumps(data=data, message=message, success=True)
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)
