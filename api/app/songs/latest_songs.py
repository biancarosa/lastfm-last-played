"""app.healthcheck.healthcheck

Module that deals with HealthCheck route."""
import logging
import os

import requests

from flask import jsonify, request

log = logging.getLogger(__name__)


def route(user):
    log.info('Received a request :: %s', request)
    api_key = os.environ.get('LASTFM_API_KEY')
    api_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={api_key}&limit=1&format=json"
    if not api_key:
        log.error('Last.fm API key is not set')
        return jsonify({
            "message": "INTERNAL_ERROR"
        }), 500
    try:
        req = requests.get(api_url)
        return jsonify(req.json()), req.status_code
    except Exception as exception:  # pylint: disable=W0703
        log.exception(exception)
        return jsonify({
            "message": "INTERNAL_ERROR"
        }), 500
