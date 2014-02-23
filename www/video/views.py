#!/usr/bin/python
from flask import Blueprint, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import login_required

video = Blueprint('video', __name__, template_folder='templates')

@video.route('/<int:video_id>', methods=['GET'])
@login_required
def get_video(video_id):
    return render_template('video/index.html', video_id=video_id)
