"""app.healthcheck.healthcheck

Module that deals with HealthCheck route."""
import logging
import os

import requests

from flask import jsonify, request

log = logging.getLogger(__name__)
BASE_URL = 'https://ws.audioscrobbler.com/2.0/'
RECENT_TRACKS_PARAMS = 'method=user.getrecenttracks&limit=1&format=json'


def route(user):
    """Returns the user two latest tracks on lastfm"""
    log.info('Received a request :: %s', request)
    api_key = os.environ.get('LASTFM_API_KEY')
    api_url = f"{BASE_URL}?{RECENT_TRACKS_PARAMS}&user={user}&api_key={api_key}"
    if not api_key:
        log.error('Last.fm API key is not set')
        return jsonify({
            "message": "INTERNAL_ERROR"
        }), 500
    try:
        req = requests.get(api_url)
        lastfm_response = req.json()
        track = lastfm_response['recenttracks']['track'][0]
        if track:
            if request.args.get('format') == 'shields.io':
                song = track['name']
                artist = track['artist']['#text']
                return jsonify({
                    'schemaVersion': 1,
                    'label': 'last-played-song',
                    'message': f"{song} - {artist}",
                }), 200
            return jsonify({
                'track': track
            }), req.status_code
        return jsonify({
            'message': 'NO_TRACKS_FOUND'
        }), 204
    except Exception as exception:  # pylint: disable=W0703
        log.exception(exception)
        return jsonify({
            'message': 'INTERNAL_ERROR'
        }), 500
