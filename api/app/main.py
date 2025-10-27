"""app.main

Module that starts the Flask application
"""
import os
import logging

from flask import Flask
from flask_cors import CORS
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource

from app.healthcheck import blueprint as health_check_blueprint
from app.songs import blueprint as songs_blueprint

LOG_FORMAT = ("%(levelname) -10s %(asctime)s %(name) "
              "-30s %(funcName) -35s %(lineno) -5d: %(message)s")

# Configure logging
logging.basicConfig(level=os.environ.get(
    'LOG_LEVEL', 'INFO'), format=LOG_FORMAT)

# Set up OpenTelemetry logging with OTLP exporter
logger_provider = LoggerProvider(
    resource=Resource.create({
        "service.name": os.environ.get('OTEL_SERVICE_NAME', 'lastfm-last-played'),
    })
)

# Add OTLP exporter for logs
otlp_exporter = OTLPLogExporter(
    endpoint=os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4318') + '/v1/logs',
)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

# Attach OTLP handler to root logger
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

# Initialize OpenTelemetry logging instrumentation (adds trace context to logs)
LoggingInstrumentor().instrument(set_logging_format=True)

# pylint: disable=C0103
app = Flask(__name__)
CORS(app)

app.register_blueprint(health_check_blueprint.create_blueprint())
app.register_blueprint(songs_blueprint.create_blueprint())
