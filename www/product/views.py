#!/usr/bin/python
from flask import Blueprint, request, render_template, redirect, url_for, \
    abort, session, flash, g, jsonify
from flask.ext.login import login_required

product = Blueprint('product', __name__, template_folder='templates')

@product.route('/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    return render_template('product/index.html', product_id=product_id)
