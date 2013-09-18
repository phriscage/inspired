"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
## need to import all child models for now
import inspired.v1.lib.videos.models
import inspired.v1.lib.video_sources.models
import inspired.v1.lib.scenes.models
import inspired.v1.lib.cast_members.models
import inspired.v1.lib.products.models
import inspired.v1.lib.ref_product_types.models
import inspired.v1.lib.ref_product_styles.models
from inspired.v1.lib.artists.models import Artist
from database import db_session
from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, jsonify, request, abort
from inspired.v1.helpers.serializers import JSONEncoder
import json

artists = Blueprint('artists', __name__)

#create routes
@artists.route('/', methods=['GET'])
#@requires_api_key
def get_all():
    """Get all the artists.

    **Example request:**

    .. sourcecode:: http

       GET /artists HTTP/1.1
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
    :statuscode 404: artists do not exist
    """
    try:
        #data, message = ([{'name': 'abc'}, {'name': 'xyz'}], 'test message')
        message = 'success'
        data = [obj.to_json for obj in Artist.query.all() if obj]
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        return jsonify(error=404, message=message, success=False), 404
    else:
        #return json.dumps(data=data, message=message, success=True)
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)


#create routes
@artists.route('/', methods=['POST'])
#@requires_api_key
def post():
    """Create a new artist.

    **Example request:**

    .. sourcecode:: http

       POST /artists/create HTTP/1.1
       Accept: application/json
        Data: { 
            'name': 'artist name',
            'fist_name', 'artist first_name',
            'last_name', 'artist last_name',
            'video_name': 'video name'
        }

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 201 Created
       Content-Type: application/json


    :statuscode 201: Created
    :statuscode 400: Bad Request
    :statuscode 409: Conflict
    """
    if not request.json or not 'name' in request.json:
        abort(400)
    try:
        artist = Artist.query.filter(Artist.name == request.json['name']).one()
        return jsonify(message='Conflict', success=True), 409
    except NoResultFound as error:
        pass
    a = Artist(name=request.json['name'])
    if 'video_name' in request.json:
        v = Video(name=request.json['video_name'])
        a.videos.append(v)
    db_session.add(a)
    db_session.commit()
    return jsonify(message='hello', success=True), 200
    


@artists.route('/<int:artist_id>', methods=['GET'])
#@requires_api_key
def get(artist_id):
    """Get a artist identified by `artist_id`.

    **Example request:**

    .. sourcecode:: http

       GET /artists/123 HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
        "name": "Joe Schmoe",
        "first_name": "Joe",
        "second_name": "Schmoe"
       }

    :statuscode 200: success
    :statuscode 404: artist does not exist
    """
    try:
        message = 'success'
        data = Artist.query.filter(Artist.id==artist_id).first()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "'%s' record does not exist." % artist_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        data = data.to_json
        #return json.dumps(data=data, message=message, success=True)
        return json.dumps(dict(data=data, message=message, success=True),
            cls=JSONEncoder)
