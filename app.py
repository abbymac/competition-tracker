import os
import json
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pytz import utc
from flask_moment import Moment
from flask_migrate import Migrate

from models import setup_db, db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  def index():
    return render_template('index.html')

  return app




APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)