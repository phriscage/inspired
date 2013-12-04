#!/usr/bin/python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')
from inspired_config import API_URL
from flask import Blueprint, render_template, redirect, url_for

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
    #return render_template('core/index.html')
    return redirect(url_for('auth.login'))

@core.route('/signup', methods=['GET'])
def signup():
    return render_template('core/signup.html', api_url=API_URL)


