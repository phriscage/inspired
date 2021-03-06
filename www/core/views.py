#!/usr/bin/python
from flask import Blueprint, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import login_required

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/', methods=['GET'])
def get_index():
    """ root path redirect to login """
    #return render_template('core/index.html')
    return redirect(url_for('auth.login'))

@core.route('/signup', methods=['GET'])
def get_signup():
    """ get the signup page """
    return render_template('core/signup.html')

@core.route('/music', methods=['GET'])
@login_required
def get_music():
    """ get the music page """
    return render_template('core/music.html')
