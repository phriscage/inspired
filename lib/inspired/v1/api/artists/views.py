"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import db_session
## need to import all child models for now
from inspired.v1.lib.artists.models import Artist
from inspired.v1.lib.videos.models import Video
from inspired.v1.api.util import crossdomain
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload, contains_eager

from flask import Blueprint, jsonify, request, abort, make_response
from inspired.v1.helpers.serializers import JSONEncoder, json_encoder
import json

artists = Blueprint('artists', __name__)

#create routes
@artists.route('', methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
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
            "name": "abc",
            "image_url": "xyz"
           },
           {
            "name": "xyz",
            "image_url": "123"
           }
         ]
       }

    :statuscode 200: success
    :statuscode 404: artists do not exist
    """
    ## columns can either be str or class Attributes, but class Attributes are
    ## required to specify columns
    columns = [Artist.name, Artist.image_url,
        Artist.videos, Video.name]
    try:
        message = 'success'
        data = Artist.query.outerjoin(Artist.videos
            ).options(
                contains_eager(Artist.videos),
            ).limit(10).all()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None or not data:
        message = "No artist data exists."
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=json_encoder(False, columns)))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response


#create routes
@artists.route('', methods=['POST'])
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
        artist = Artist.query.filter(Artist.name == request.json['name']).first()
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


@artists.route('/<int:artist_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
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
        "second_name": "Schmoe",
        "image_url": "abc"
       }

    :statuscode 200: success
    :statuscode 404: artist does not exist
    """
    ## columns can either be str or class Attributes, but class Attributes are
    ## required to specify columns
    columns = [Artist.name, Artist.first_name, Artist.last_name, 
        Artist.image_url, 
        Artist.videos, Video.name]
    try:
        message = 'success'
        data = Artist.query.outerjoin(Artist.videos
        #data = db_session.query(*columns).outerjoin(Artist.videos
            ).options(
                contains_eager(Artist.videos),
            ).filter(Artist.id==artist_id
            ).first()
    except NoResultFound as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 404
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500

    if data is None:
        message = "'%s' record does not exist." % artist_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=json_encoder(False, columns)))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response
