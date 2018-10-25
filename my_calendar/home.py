from flask.blueprints import Blueprint
from flask import render_template, session
from random import getrandbits


bp_home = Blueprint('home', __name__, url_prefix='/')


@bp_home.route('/')
def home():
    csrf_token = hex(getrandbits(32))
    session['csrf_token'] = csrf_token
    return render_template('home.html', csrf_token=csrf_token)
