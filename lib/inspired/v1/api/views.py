"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
from flask import Blueprint, jsonify
from inspired.v1.helpers.lazy_view import LazyView
from product_types.views import product_types

api_v1 = Blueprint('api_v1', __name__, url_prefix='/test')

@api_v1.app_errorhandler(400)
@api_v1.app_errorhandler(404)
@api_v1.app_errorhandler(405)
@api_v1.app_errorhandler(500)
def default_error_handle(error=None):
    """ handle all errors with json output """
    return jsonify(error=error.code, message=error.message, success=False), \
        error.code

#api_v1.add_url_rule('/product_types', methods=['GET'],
    #view_func=LazyView('inspired.v1.api.handlers.get_images'))
