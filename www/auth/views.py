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
            #return jsonify(url=url_for('core.signup'), success=True, code=302)
            message = "Unknown email_address or password"
            print "User DNE"
            return jsonify(message=message, success=True, code=400)
        if user.check_password(request.json['password']):
            login_user(user)
            #flash("'%s' logged in successfully." % user.email_address)
            return jsonify(url=url_for('user.settings', user_id=user.id), 
                success=True, code=302)
        else:
            message = "Unknown email_address or password"
            print "Password incorrect"
            return jsonify(message=message, success=True, code=400)
        #return redirect(url_for('user.settings', user_id=user.id))
    else:
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('user.settings', user_id=g.user.id))
        return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    """ logout the user and redirect to home """
    logout_user()
    return redirect(url_for('core.index'))
