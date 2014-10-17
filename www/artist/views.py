#!/usr/bin/python
from flask import Blueprint, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import login_required

artist = Blueprint('artist', __name__, template_folder='templates')

@artist.route('/<int:artist_id>', methods=['GET'])
@login_required
def get_artist(artist_id):
    return render_template('artist/index.html', artist_id=artist_id)
