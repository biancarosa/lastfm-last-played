"""app.main

Module that starts the Flask application
"""
import os
import logging

from flask import Flask
from flask_cors import CORS

from app.healthcheck import blueprint as health_check_blueprint
from app.songs import blueprint as songs_blueprint

LOG_FORMAT = ("%(levelname) -10s %(asctime)s %(name) "
              "-30s %(funcName) -35s %(lineno) -5d: %(message)s")
logging.basicConfig(level=os.environ.get(
    'LOG_LEVEL', 'INFO'), format=LOG_FORMAT)

# pylint: disable=C0103
app = Flask(__name__)
CORS(app)
app.register_blueprint(health_check_blueprint.create_blueprint())
app.register_blueprint(songs_blueprint.create_blueprint())
