"""app.healthcheck.healthcheck

Module that deals with HealthCheck route."""
import logging

from flask import jsonify

log = logging.getLogger(__name__)


def route():
    """Returns health information"""
    log.info("Healthcheck was requested")
    return jsonify({
        "message": "Hello. Is it me you're looking for?"
    })
