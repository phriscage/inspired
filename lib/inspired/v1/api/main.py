#!/usr/bin/python
"""
API bootstrap file
"""
from flask import Flask, jsonify
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../lib')
sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/../../../../conf')

from inspired_config import SQLALCHEMY_DATABASE_URI
from database import init_engine, db_session


def create_app(uri):
    """ dynamically create the app """
    app = Flask(__name__)
    #app.config.from_pyfile(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_recycle=3600)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(500)
    def default_error_handle(error=None):
        """ handle all errors with json output """
        return jsonify(error=error.code, message=str(error), success=False),\
            error.code

    ## add each api Blueprint and create the base route
    from inspired.v1.api.artists.views import artists
    from inspired.v1.api.product_types.views import product_types
    from inspired.v1.api.users.views import users
    from inspired.v1.api.scenes.views import scenes
    from inspired.v1.api.videos.views import videos
    from inspired.v1.api.products.views import products
    from inspired.v1.api.product_styles.views import product_styles
    app.register_blueprint(artists, url_prefix="/api/v1/artists")
    app.register_blueprint(product_types, url_prefix="/api/v1/product_types")
    app.register_blueprint(users, url_prefix="/api/v1/users")
    app.register_blueprint(scenes,url_prefix="/api/v1/scene")
    app.register_blueprint(videos, url_prefix="/api/v1/video")
    app.register_blueprint(products, url_prefix="/api/v1/products")
    app.register_blueprint(product_styles, url_prefix="/api/v1/product_styles")

    return app


def bootstrap(**kwargs):
    """bootstraps the application. can handle setup here"""
    app = create_app(SQLALCHEMY_DATABASE_URI)
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
