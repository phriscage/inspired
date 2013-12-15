#!/usr/bin/python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../lib')
from database import db_session
from flask import Blueprint, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import logout_user, current_user, login_user
from inspired.v1.lib.users.models import User
from sqlalchemy.orm.exc import NoResultFound
from main import facebook

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ check if the request data exists with the correct values, then check 
        if the User exists and the password matches else redirect to the 
        signup page.
    """
    if request.method == 'POST':
        if not request.json:
            abort(400)
        for var in ['email_address', 'password']:
            if var not in request.json:
                abort(400)
        try:
            user = User.query.filter(User.email_address == \
                request.json['email_address']).one()
        except NoResultFound as error:
            user = User(**request.json)
            db_session.add(user)
            db_session.commit()
            login_user(user)
            message = 'Created: %s' % user.email_address
            return jsonify(url=url_for('core.get_music'), success=True)
        if user.check_password(request.json['password']):
            login_user(user)
            #flash("'%s' logged in successfully." % user.email_address)
            return jsonify(url=url_for('core.get_music'), success=True)
        else:
            message = "Unknown email_address or password"
            print "Password incorrect"
            return jsonify(message=message, success=True)
        #return redirect(url_for('user.settings', user_id=user.id))
    else:
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('core.get_music'))
        return render_template('auth/login.html')

@auth.route('/logout', methods=['GET'])
def get_logout():
    """ logout the user and redirect to home """
    logout_user()
    session.pop('logged_in', None)
    session.pop('facebook_token', None)
    return redirect(url_for('core.get_index'))

@auth.route('/login/facebook', methods=['GET'])
def get_login_facebook():
    """ testing the facebook login """
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('core.get_music'))
    return facebook.authorize(callback=url_for(
        'auth.get_login_facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@auth.route('/login/facebook/authorized', methods=['GET'])
@facebook.authorized_handler
def get_login_facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if 'access_token' in resp:
        session['oauth_token'] = (resp['access_token'], '')
    else:
        print resp
    if 'oauth_token' in session:
        me = facebook.get('/me')
        #print me.data
        try:
            user = User.query.filter(User.email_address == \
                me.data['email']).one()
            if not user.facebook_id or not user.first_name or \
                not user.last_name:
                if not user.facebook_id:
                    user.facebook_id =  me.data['id']
                if not user.first_name:
                    user.first_name =  me.data['first_name']
                if not user.last_name:
                    user.last_name =  me.data['last_name']
                db_session.commit()
            #print "User already exists."
            #return redirect(url_for('auth.login'))
        except NoResultFound as error:
            fb_data = { 
                'email_address': me.data['email'],
                'first_name': me.data['first_name'],
                'last_name': me.data['last_name'],
                'facebook_id': me.data['id']
            }
            user = User(**fb_data)
            db_session.add(user)
            db_session.commit()
        login_user(user)
        return redirect(url_for('core.get_music'))
        #return "Logged in as '%s' redirect=%s" % \
            #(me.data, request.args.get('next'))
    else:
        print "No oauth_token"
        return redirect(url_for('auth.get_login'))

