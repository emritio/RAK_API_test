from flask import Blueprint, render_template, redirect, url_for, jsonify

apilog_blueprint = Blueprint('apilog', __name__, url_prefix='/')
#The main page routes to index.html
@apilog_blueprint.route('/')
def index():
    return render_template('index.html')



