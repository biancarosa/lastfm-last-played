"""app.healthcheck.healthcheck

Module that deals with HealthCheck route."""
import logging

from flask import jsonify
from opentelemetry import trace

log = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def route():
    """Returns health information"""
    with tracer.start_as_current_span("healthcheck_route") as span:
        span.set_attribute("service.name", "healthcheck")
        return jsonify({
            "message": "Hello. Is it me you're looking for?"
        })
