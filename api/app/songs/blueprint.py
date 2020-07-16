"""app.auth.blueprint

Module that deals with Blueprint-related stuff."""
from flask import Blueprint
from app.songs import latest_songs


def create_blueprint():
    """Creates a Blueprint"""
    blueprint = Blueprint('Songs Blueprint', __name__)
    blueprint.route(
        '/<user>/latest-song', methods=['GET'])(latest_songs.route)
    return blueprint
