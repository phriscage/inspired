"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

import inspired.v1.lib.videos.models
import inspired.v1.lib.video_sources.models
import inspired.v1.lib.scenes.models
import inspired.v1.lib.cast_members.models
import inspired.v1.lib.products.models
import inspired.v1.lib.ref_product_types.models
import inspired.v1.lib.ref_product_styles.models

from inspired.v1.lib.scenes.models import Scene
from database import db_session
from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, jsonify, request, abort
from inspired.v1.helpers.serializers import JSONEncoder

import json

scenes = Blueprint('scene', __name__)

@scenes.route('/<int:scene_id>', methods=['GET'])
#@requires_api_key
def get(scene_id):
    """Get a scene identified by `scene_id`.

    **Example request:**

    .. sourcecode:: http

       GET /scenes/123 HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

    :statuscode 200: success
    :statuscode 404: scene does not exist
    """
    try:
        message = 'success'
        data = Scene.query.filter(Scene.id==scene_id).first()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "'%s' record does not exist." % scene_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        data = data.to_json
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)
