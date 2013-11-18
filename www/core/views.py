#!/usr/bin/python
from flask import Blueprint, render_template
#from flask import Blueprint, render_template, redirect, url_for

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
    return render_template('index.html')
    #return redirect(url_for('auth.login'))

