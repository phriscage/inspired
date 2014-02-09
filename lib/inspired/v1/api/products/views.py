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
from inspired.v1.lib.ref_product_types.models import RefProductType
from inspired.v1.lib.ref_product_styles.models import RefProductStyle
from inspired.v1.lib.product_images.models import ProductImage
from inspired.v1.lib.product_retailers.models import ProductRetailer
from inspired.v1.lib.retailers.models import Retailer
from inspired.v1.api.util import crossdomain
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload, contains_eager


from flask import Blueprint, jsonify, request, abort, make_response
from inspired.v1.helpers.serializers import JSONEncoder, json_encoder
import json

products = Blueprint('products', __name__)

#create routes
@products.route('', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST'], headers='Content-Type')
#@requires_api_key
def post():
    """Create a new product.

    **Example request:**

    .. sourcecode:: http

       POST /products/create HTTP/1.1
       Accept: application/json
        data = {
            'brand': 'abc',
            'model': 'abc',
            'upc': '123',
            'product_type': {
                'id': 1,
            },
            'product_style': {
                'id': 2,
            },
            'product_images': [{
                'url': 'http://abc/asdf.png',
            }, {
                'url': '/static/item.png',
            }]
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
    for var in ['brand', 'model', 'upc', 'product_type', 'product_style', 
        'product_images']:
        if var not in request.json:
            abort(400)
        if var in ['product_type', 'product_style']:
            if 'id' not in request.json[var]:
                abort(400)
    if type(request.json['product_images']) is not list:
        abort(400)
    if len(request.json['product_images']) > 5:
        abort(400)
    try:
        product = Product.query.filter(Product.upc==request.json['upc']).one()
        return jsonify(message='Conflict', success=False), 409
    except NoResultFound as error:
        pass
    try:
        product_type = RefProductType.query.filter(
            RefProductType.id==request.json['product_type']['id']).one()
        del(request.json['product_type'])
    except NoResultFound as error:
        return jsonify(message="Product Type '%s' Not Found" % 
            request.json['product_type']['id'], success=False), 404
    try:
        product_style = RefProductStyle.query.filter(
            RefProductStyle.id==request.json['product_style']['id']).one()
        del(request.json['product_style'])
    except NoResultFound as error:
        return jsonify(message="Product Style '%s' Not Found" % 
            request.json['product_style']['id'], success=False), 404
    product_image_data = request.json['product_images']
    del(request.json['product_images'])
    product = Product(product_type=product_type, product_style=product_style, 
        **request.json)
    product_images = [ProductImage(product=product, **data) \
        for data in product_image_data]
    product.product_images = product_images
    db_session.add(product)
    db_session.commit()
    message = 'Created: %s' % product.upc
    data = dict(id=product.id, upc=product.upc)
    return jsonify(message=message, data=data, success=True), 201
    

@products.route('/<int:product_id>', methods=['GET', 'OPTIONS'])
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
            'brand': 'abc',
            'upc': '123'
            ...
        }

    :statuscode 200: success
    :statuscode 404: product does not exist
    """
    ## columns can either be str or class Attributes, but class Attributes are 
    ## required to specify columns
    columns = [Product.upc, Product.brand, Product.model,
        Product.product_type, RefProductType.name, 
        Product.product_style, RefProductStyle.name,
        Product.product_images, ProductImage.url,
        Product.product_retailers, ProductRetailer.url, ProductRetailer.price,
        ProductRetailer.retailer, Retailer.name, Retailer.image_url]
    try:
        message = 'success'
        ## INNER JOIN any relationship in 'join()' and LEFT OUTER JOIN any other
        ## relationship in 'outerjoin()'. contains_eager will eager load the 
        ## columns and you need to include indirect relationships in one ().
        data = Product.query.join(Product.product_type, Product.product_style,
            Product.product_retailers, ProductRetailer.retailer
            ).outerjoin(Product.product_images
            ).options(
                contains_eager(Product.product_type), 
                contains_eager(Product.product_style),
                contains_eager(Product.product_images),
                contains_eager(Product.product_retailers),
                contains_eager(Product.product_retailers, 
                    ProductRetailer.retailer),
            ).filter(Product.id==product_id
            ).one()
        ## TODO need to determine best method to parse the NamedTuple for
        ## selecting specific columns
        #data = db_session.query(*columns).join(Product.product_type, 
            #Product.product_style
            #).outerjoin(Product.product_images
            #).filter(Product.id==product_id
            #).one()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "'%s' record does not exist." % product_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=json_encoder(False, columns)))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response
