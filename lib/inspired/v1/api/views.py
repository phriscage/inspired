"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
from flask import Blueprint, jsonify
from inspired.v1.helpers.lazy_view import LazyView

api_v1 = Blueprint('api_v1', __name__)

@api_v1.app_errorhandler(400)
@api_v1.app_errorhandler(404)
@api_v1.app_errorhandler(405)
@api_v1.app_errorhandler(500)
def default_error_handle(error=None):
    """ handle all errors with json output """
    return jsonify(error=error.code, message=error.message, success=False), \
        error.code

api_v1.add_url_rule('/images', methods=['GET'],
    view_func=LazyView('inspired.v1.api.handlers.get_images'))
api_v1.add_url_rule('/images/urls', methods=['POST'],
    view_func=LazyView('inspired.v1.api.handlers.create_image_urls'))
api_v1.add_url_rule('/image/random', methods=['GET'], 
    view_func=LazyView('inspired.v1.api.handlers.get_image_random'))
api_v1.add_url_rule('/image/<int:image_id>', methods=['GET'], 
    view_func=LazyView('inspired.v1.api.handlers.get_image'))
