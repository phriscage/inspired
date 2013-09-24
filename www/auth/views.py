#!/usr/bin/python
from flask import Blueprint, render_template, redirect, url_for, g
from flask.ext.login import logout_user

app = Blueprint('auth', __name__, template_folder='templates')

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('user.settings'))
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    #return redirect(url_for('login'))
    return redirect(url_for('app.index'))

