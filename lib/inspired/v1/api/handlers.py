"""
    handlers file contains all the methods for the app views
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__) + '/../../../')

from inspired.v1.lib.images import Images
from flask import jsonify, request

images = Images()

def get_image(image_id):
    """ get_image """
    try:
        url, message = images.get_image(image_id)
    except Exception, error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if url is None:
        return jsonify(error=404, message=message, success=False), 404
    else:
        return jsonify(url=url, message=message, success=True)


def get_image_random():
    """ get_image_random """
    try:
        url, message = images.get_image_random()
    except Exception, error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if url is None:
        return jsonify(error=404, message=message, success=False), 404
    else:
        return jsonify(url=url, message=message, success=True)


def get_images(start=None, limit=None):
    """ get_images """
    if request.args.get('start'):
        limit = request.args.get('start')
    if request.args.get('limit'):
        limit = request.args.get('limit')
    try:
        urls, message = images.get_images(start, limit)
    except ValueError, error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 400
    except Exception, error:
        message = '%s: %s' % (error.__class__.__name__, error)
        return jsonify(message=message, success=False), 500
    if urls is None:
        return jsonify(error=404, message=message, success=False), 404
    else:
        return jsonify(urls=urls, message=message, success=True) 
