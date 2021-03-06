"""
    views file contains all the routes for the app and maps them to a
    specific hanlders function.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import db_session
## need to import all child models for now
from inspired.v1.lib.users.models import User
from inspired.v1.api.util import crossdomain
from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, jsonify, request, abort, make_response
from inspired.v1.helpers.serializers import JSONEncoder
import json

users = Blueprint('users', __name__)

#create routes
@users.route('', methods=['POST', 'OPTIONS'])
@crossdomain(origin="*", methods=['POST', 'OPTIONS'], headers='Content-Type')
#@requires_api_key
def post():
    """Create a new user.

    **Example request:**

    .. sourcecode:: http

       POST /users/create HTTP/1.1
       Accept: application/json
        data = {
            'email_address': 'abc.com',
            'first_name': 'Joe',
            'last_name': 'Schome'
        }

    **Example response:**

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json
        data: {'id': <user id> }


    :statuscode 201: Created
    :statuscode 400: Bad Request
    :statuscode 409: Conflict
    """
    if not request.json or 'email_address' not in request.json or \
        'password' not in request.json:
        abort(400)
    try:
        user = User.query.filter(User.email_address == \
            request.json['email_address']).one()
        return jsonify(message='Conflict', success=True), 409
    except NoResultFound as error:
        pass
    user = User(**request.json)
    db_session.add(user)
    db_session.commit()
    message = 'Created: %s' % user.email_address
    data = dict(id=user.id, email_address=user.email_address)
    return jsonify(message=message, data=data, success=True), 201
    

@users.route('/<int:user_id>', methods=['GET'])
@crossdomain(origin="*", methods=['GET'], headers='Content-Type')
#@requires_api_key
def get(user_id):
    """Get a user identified by `user_id`.

    **Example request:**

    .. sourcecode:: http

       GET /users/123 HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

        data = {
            'email_address': 'abc.com',
            'first_name': 'Joe',
            'last_name': 'Schome',
            ...
        }

    :statuscode 200: success
    :statuscode 404: user does not exist
    """
    try:
        message = 'success'
        data = User.query.filter(User.id==user_id).first()
    except Exception as error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if data is None:
        message = "'%s' record does not exist." % user_id
        return jsonify(error=404, message=message, success=False), 404
    else:
        ## need to use the JSONEncoder class for datetime objects
        data = data.to_json
        response = make_response(json.dumps(dict(data=data, message=message,
            success=True), cls=JSONEncoder))
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response


@users.route('/<int:user_id>/password', methods=['PUT', 'PATCH', 'OPTIONS'])
@crossdomain(origin="*", methods=['PUT', 'PATCH'], headers='Content-Type')
#@requires_api_key
def patch_password(user_id):
    """Update a user password identified by `user_id`.

    **Example request:**

    .. sourcecode:: http

       GET /users/123 HTTP/1.1
       Accept: application/json

    **Example response:**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

        data = {
            'old_password': 'abc',
            'new_password': 'xyz'
        }

    :statuscode 200: success
    :statuscode 404: user does not exist
    """
    if not request.json:
        return jsonify(message="Not JSON", success=False), 400
    for var in ['api_key', 'old_password', 'new_password']:
        if var not in request.json:
            message = "%s is missing in the payload" % var
            return jsonify(message=message, success=False), 400
    try:
        user = User.query.filter(User.id==user_id, 
            User.api_key==request.json['api_key']).one()
    except NoResultFound as error:
        return jsonify(message=None, success=False), 401
    if not user.check_password(request.json['old_password']):
        print "bad password"
        return jsonify(message=None, success=False), 400
    else:
        ## need to use the JSONEncoder class for datetime objects
        user.set_password(request.json['new_password'])
        db_session.add(user)
        db_session.commit()
        message = "Successfully changed password."
        return jsonify(message=message, success=True)
