"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')

import inspired.v1.lib.videos.models
import inspired.v1.lib.video_sources.models
import inspired.v1.lib.videos.models
import inspired.v1.lib.cast_members.models
import inspired.v1.lib.products.models
import inspired.v1.lib.ref_product_types.models
import inspired.v1.lib.ref_product_styles.models

from inspired.v1.lib.videos.models import Video
from inspired.v1.lib.scenes.models import Scene
from database import db_session
from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, jsonify, request, abort
from inspired.v1.helpers.serializers import JSONEncoder

import json

videos = Blueprint('video', __name__)

@videos.route('/<int:video_id>', methods=['GET'])
#@requires_api_key
def get(video_id):
    """Get a video identified by `video_id`.

    **Example request:**

    .. sourcecode:: http

       GET /videos/1/ HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

    :statuscode 200: success
    :statuscode 404: video does not exist
    """
    try:
        message = 'success'
        data = Video.query.filter(Video.id==video_id).first()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "'%s' record does not exist." % video_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        data = data.to_json
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)


@videos.route('/<int:video_id>/scenes', methods=['GET'])
#@requires_api_key
def get_all_scene(video_id):
    """Get all scenen contain the `video_id`.

    **Example request:**

    .. sourcecode:: http

       GET /videos/1/scenes HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

    :statuscode 200: success
    :statuscode 404: video does not exist
    """
    try:
        message = 'success'
        results = Scene.query.filter(Scene.video_id==video_id).all()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if results is None:
        message = "'%s' record does not exist." % video_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        data = []
        for item in results:
            data.append(item.to_json)
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)
