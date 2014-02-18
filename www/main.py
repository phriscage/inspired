#!/usr/bin/python
"""
UI bootstrap file
"""
import sys
import os
import argparse
from flask import Flask, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import LoginManager, current_user

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')

from inspired_config import SQLALCHEMY_DATABASE_URI, FACEBOOK_APP_ID, \
    FACEBOOK_APP_SECRET, API_URL
from database import init_engine, db_session
from flask_oauthlib.client import OAuth

login_manager = LoginManager()

from inspired.v1.lib.users.models import User

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

oauth = OAuth()
facebook = oauth.remote_app(
    'facebook',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    app_key='FACEBOOK'
)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

def create_app(uri):
    """ dynamically create the app """
    app = Flask(__name__, static_url_path='/static', static_folder='./static')
    #app.config.from_pyfile(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_recycle=3600)
    app.secret_key = ('\xda\xe0\xff\xc8`\x99\x93e\xd0\xb9\x0e\xc9\xde\x84?q'
        '\x9e\x19\xc0\xa1\xa7\xfb\xd0\xde')
    login_manager.init_app(app)
    oauth.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.before_request
    def before_request():
        g.user = current_user
        g.api_url = API_URL

    @app.errorhandler(401)
    def unauthorized_error_handle(error=None):
        """ handle all unauthorized_errors with redirect to login """
        return redirect(url_for('auth.login'))

    import core.views
    import auth.views 
    import user.views 
    import product.views
    import artist.views
    #app.register_blueprint(landing.app)
    app.register_blueprint(core.views.core)
    app.register_blueprint(auth.views.auth, url_prefix='/auth')
    app.register_blueprint(user.views.user, url_prefix='/user')
    app.register_blueprint(product.views.product, url_prefix='/product')
    app.register_blueprint(artist.views.artist, url_prefix='/artist')

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
        dest="port", type=int, default=8080)
    kwargs = parser.parse_args()
    bootstrap(**kwargs.__dict__)
