"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import db_session
## need to import all child models for now
from inspired.v1.lib.videos.models import Video
from inspired.v1.lib.video_sources.models import VideoSource
from inspired.v1.lib.products.models import Product
from inspired.v1.api.util import crossdomain
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload, contains_eager

from flask import Blueprint, jsonify, request, abort, make_response
from inspired.v1.helpers.serializers import JSONEncoder, json_encoder
import json

videos = Blueprint('videos', __name__)

#create routes
@videos.route('', methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
#@requires_api_key
def get_all():
    """Get all the videos.

    **Example request:**

    .. sourcecode:: http

       GET /videos HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
         "data": [
           {
            "name": "abc",
           },
           {
            "name": "xyz",
           }
         ]
       }

    :statuscode 200: success
    :statuscode 404: videos do not exist
    """
    ## columns can either be str or class Attributes, but class Attributes are
    ## required to specify columns
    columns = [Video.name,
        #Video.products, Product.upc]
	Video.video_sources, VideoSource.name, VideoSource.url]
    try:
        message = 'success'
        data = Video.query.outerjoin(Video.video_sources
            ).options(
                contains_eager(Video.video_sources),
            ).limit(10).all()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None or not data:
        message = "No video data exists."
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=json_encoder(False, columns)))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response


@videos.route('/<int:video_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
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

       {
        "name": "Joe Schmoe",
        "first_name": "Joe",
        "second_name": "Schmoe",
        "image_url": "abc"
       }

    :statuscode 200: success
    :statuscode 404: video does not exist
    """
    ## columns can either be str or class Attributes, but class Attributes are
    ## required to specify columns
    columns = [Video.name,
        Video.video_sources, VideoSource.name, VideoSource.url,
        Video.products, Product.upc]
    try:
        message = 'success'
        data = Video.query.outerjoin(Video.video_sources, Video.products
            ).options(
                contains_eager(Video.video_sources),
                contains_eager(Video.products),
            ).filter(Video.id==video_id
            ).first()
    except NoResultFound as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 404
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500

    if data is None:
        message = "'%s' record does not exist." % video_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=json_encoder(False, columns)))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response


@videos.route('/<int:video_id>/scenes', methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
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
