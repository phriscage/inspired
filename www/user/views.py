#!/usr/bin/python
from flask import Blueprint, render_template, request
from flask.ext.login import login_required

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/<int:user_id>/settings')
@login_required
def settings(user_id):
    return render_template('user/settings.html', user_id=user_id)
