#!/usr/bin/python
from flask import Blueprint, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import login_required

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/<int:user_id>/settings', methods=['GET'])
@login_required
def get_settings(user_id):
    ## only the same authenticated user can access their settings
    if user_id != g.user.id:
        return redirect(url_for('user.get_settings', user_id=g.user.id))
    return render_template('user/settings.html', user_id=user_id)

#@user.route('/<int:user_id>/settings/my-profile', methods=['GET'])
@user.route('/settings/my-profile', methods=['GET'])
@login_required
def get_my_profile():
    """ get the my-profile page """
    return render_template('user/settings/my-profile.html')

@user.route('/settings/email-preferences', methods=['GET'])
@login_required
def get_email_preferences():
    """ get the email-preferences page """
    return render_template('user/settings/email-preferences.html')

@user.route('/settings/invite-friends', methods=['GET'])
@login_required
def get_invite_friends():
    """ get the invite-friends page """
    return render_template('user/settings/invite-friends.html')

@user.route('/settings/send-feedback', methods=['GET'])
@login_required
def get_send_feedback():
    """ get the send-feedback page """
    return render_template('user/settings/send-feedback.html')

@user.route('/settings/help', methods=['GET'])
@login_required
def get_help():
    """ get the help page """
    return render_template('user/settings/help.html')

@user.route('/settings/legal', methods=['GET'])
@login_required
def get_legal():
    """ get the legal page """
    return render_template('user/settings/legal.html')
