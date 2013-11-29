"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from inspired.v1.lib.ref_product_styles.models import RefProductStyle

from flask import Blueprint, jsonify, request
from inspired.v1.helpers.lazy_view import LazyView
from inspired.v1.helpers.serializers import JSONEncoder
import json

product_styles = Blueprint('product_styles', __name__)

#create routes
@product_styles.route('', methods=['GET'])
#@requires_api_key
def get_all():
    """Get all the product_styles.

    **Example request:**

    .. sourcecode:: http

       GET /product_styles HTTP/1.1
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
    :statuscode 404: product_styles do not exist
    """
    columns = ['id', 'name']
    ## sqlalchemy query requires a column obj 
    column_objs = [getattr(RefProductStyle, col) for col in columns]
    try:
        message = 'success'
        ## _asdict() is not available until sqlalchemy >= 0.8.0 
        #data = [col._asdict() for col in 
            #RefProductStyle.query.with_entities(*columns)]
        data = [dict([(key,value.__dict__[key]) for key in columns])
            for value in RefProductStyle.query.with_entities(*column_objs)]
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "No product_styles data exists."
        return jsonify(error=404, message=message, success=False), 404
    else:
        #return json.dumps(data=data, message=message, success=True)
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)


@product_styles.route('/<int:product_style_id>', methods=['GET'])
#@requires_api_key
def get(product_style_id):
    """Get a product_style identified by `product_style_id`.

    **Example request:**

    .. sourcecode:: http

       GET /product_styles/123 HTTP/1.1
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
    :statuscode 404: product_style does not exist
    """
    try:
        message = 'success'
        data = RefProductStyle.query.filter(
            RefProductStyle.id==product_style_id).first()
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
