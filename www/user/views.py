#!/usr/bin/python
from flask import Blueprint, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import login_required

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/<int:user_id>/settings')
@login_required
def settings(user_id):
    ## only the same authenticated user can access their settings
    if user_id != g.user.id:
        return redirect(url_for('user.settings', user_id=g.user.id))
    return render_template('user/settings.html', user_id=user_id)
    
