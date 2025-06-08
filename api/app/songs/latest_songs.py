"""app.healthcheck.healthcheck

Module that deals with HealthCheck route."""
import logging
import os

import requests
from flask import jsonify, request
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

log = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

BASE_URL = 'https://ws.audioscrobbler.com/2.0/'
RECENT_TRACKS_PARAMS = 'method=user.getrecenttracks&limit=1&format=json'
TIMEOUT = 1 # seconds

def _handle_error(span, error_type, message, status_code, exception=None):
    """Helper function to handle errors consistently"""
    log.error(message)
    span.set_status(Status(StatusCode.ERROR))
    if exception:
        span.record_exception(exception)
    return jsonify({"message": error_type}), status_code

def _validate_api_key(span):
    """Validate that the API key is available"""
    api_key = os.environ.get('LASTFM_API_KEY')
    if not api_key:
        return None, _handle_error(span, "INTERNAL_ERROR", 'Last.fm API key is not set', 500, Exception("Last.fm API key not set"))
    return api_key, None

def _make_lastfm_request(api_url, span):
    """Make request to Last.fm API"""
    try:
        req = requests.get(api_url, timeout=TIMEOUT)
        lastfm_response = req.json()
        span.set_attribute("lastfm.status_code", req.status_code)
        log.info("Response received", extra={'response': lastfm_response})
        return lastfm_response, req.status_code, None
    except requests.exceptions.Timeout:
        return None, None, _handle_error(span, "TIMEOUT", "Request to Last.fm timed out", 504, TimeoutError("Request to Last.fm timed out"))

def route(user):
    """Returns the user two latest tracks on lastfm"""
    with tracer.start_as_current_span("get_latest_song") as span:
        span.set_attribute("user", user)
        log.info('Received a request :: %s', request)

        # Validate API key
        with tracer.start_as_current_span("check_api_key") as api_key_span:
            api_key, error_response = _validate_api_key(api_key_span)
            if error_response:
                return error_response

        # Make API request
        api_url = f"{BASE_URL}?{RECENT_TRACKS_PARAMS}&user={user}&api_key={api_key}"
        try:
            with tracer.start_as_current_span("lastfm_api_request") as request_span:
                request_span.set_attribute("lastfm.api.url", BASE_URL)
                request_span.set_attribute("lastfm.user", user)
                
                lastfm_response, status_code, error_response = _make_lastfm_request(api_url, request_span)
                if error_response:
                    return error_response

            # Process response
            with tracer.start_as_current_span("process_response") as process_span:
                try:
                    recent_tracks = lastfm_response['recenttracks']
                except KeyError:
                    log.info("User likely doesnt exist %s", user)
                    process_span.set_status(Status(StatusCode.ERROR))
                    process_span.record_exception(KeyError("recenttracks not found in response"))
                    return jsonify({'message': 'USER_LIKELY_DOESNT_EXIST'}), 404

                try:
                    track = recent_tracks['track'][0]
                    process_span.set_attribute("track.name", track['name'])
                    process_span.set_attribute("track.artist", track['artist']['#text'])
                except IndexError:
                    process_span.set_status(Status(StatusCode.ERROR))
                    process_span.record_exception(IndexError("No tracks found"))
                    return jsonify({'message': 'NO_TRACKS_FOUND'}), 200

                # Return appropriate response format
                if request.args.get('format') == 'shields.io':
                    song = track['name']
                    artist = track['artist']['#text']
                    return jsonify({
                        'schemaVersion': 1,
                        'label': 'Last.FM Last Played Song',
                        'message': f"{song} - {artist}"
                    }), 200
                
                return jsonify({'track': track}), status_code
                
        except Exception as exception: # pylint: disable=broad-exception-caught
            log.exception(exception)
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(exception)
            return jsonify({'message': 'INTERNAL_ERROR'}), 500
