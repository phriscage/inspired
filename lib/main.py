#!/usr/bin/python
"""
API bootstrap file
"""
from flask import Flask, jsonify
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')

app = Flask(__name__)

from database import db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def default_error_handle(error=None):
    """ handle all errors with json output """
    return jsonify(error=error.code, message=error.message, success=False), \
        error.code

## add each api Blueprint and create the base route
from inspired.v1.api.artists.views import artists
from inspired.v1.api.product_types.views import product_types
app.register_blueprint(artists, url_prefix="/api/v1/artists")
app.register_blueprint(product_types, url_prefix="/api/v1/product_types")

def bootstrap(**kwargs):
    """bootstraps the application. can handle setup here"""
    app.debug = True
    app.run(host=kwargs['host'], port=kwargs['port'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Hostname or IP address",
        dest="host", type=str, default='0.0.0.0')
    parser.add_argument("--port", help="Port number",
        dest="port", type=int, default=8000)
    kwargs = parser.parse_args()
    bootstrap(**kwargs.__dict__)
