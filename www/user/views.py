#!/usr/bin/python
from flask import Blueprint, render_template, request
from flask.ext.login import login_required

app = Blueprint('user', __name__, template_folder='templates')

@app.route('/<int:user_id>/settings')
@login_required
def settings(user_id):
    return render_template('user/settings.html', user_id=user_id)
