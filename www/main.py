#!/usr/bin/python
"""
UI bootstrap file
"""
import sys
import os
import argparse
from flask import Flask, jsonify, g
from flask.ext.login import LoginManager, current_user

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')

from inspired_config import SQLALCHEMY_DATABASE_URI
from database import init_engine, db_session

login_manager = LoginManager()

from inspired.v1.lib.users.models import User

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


def create_app(uri):
    """ dynamically create the app """
    app = Flask(__name__, static_url_path='/static', static_folder='./static')
    #app.config.from_pyfile(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_recycle=3600)
    app.secret_key = ('\xda\xe0\xff\xc8`\x99\x93e\xd0\xb9\x0e\xc9\xde\x84?q'
        '\x9e\x19\xc0\xa1\xa7\xfb\xd0\xde')
    login_manager.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.before_request
    def before_request():
        g.user = current_user

    import core.views
    import auth.views 
    import user.views 
    #app.register_blueprint(landing.app)
    app.register_blueprint(core.views.core)
    app.register_blueprint(auth.views.auth, url_prefix='/auth')
    app.register_blueprint(user.views.user, url_prefix='/user')

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
