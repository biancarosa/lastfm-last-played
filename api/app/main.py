"""app.main

Module that starts the Flask application
"""
import os
import logging

from flask import Flask
from flask_cors import CORS
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace, metrics

from app.healthcheck import blueprint as health_check_blueprint
from app.songs import blueprint as songs_blueprint

LOG_FORMAT = ("%(levelname) -10s %(asctime)s %(name) "
              "-30s %(funcName) -35s %(lineno) -5d: %(message)s")

# Configure logging
logging.basicConfig(level=os.environ.get(
    'LOG_LEVEL', 'INFO'), format=LOG_FORMAT)

# Create shared resource for all telemetry
resource = Resource.create({
    "service.name": os.environ.get('OTEL_SERVICE_NAME', 'lastfm-last-played'),
})

# Set up OpenTelemetry logging with OTLP exporter
logger_provider = LoggerProvider(resource=resource)

# Add OTLP exporter for logs
otlp_log_exporter = OTLPLogExporter(
    endpoint=os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4318') + '/v1/logs',
)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))

# Attach OTLP handler to root logger to export all logs via OTLP
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

# Set up OpenTelemetry tracing with OTLP exporter
tracer_provider = TracerProvider(resource=resource)
otlp_trace_exporter = OTLPSpanExporter(
    endpoint=os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4318') + '/v1/traces',
)
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
trace.set_tracer_provider(tracer_provider)

# Set up OpenTelemetry metrics with OTLP exporter
otlp_metric_exporter = OTLPMetricExporter(
    endpoint=os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4318') + '/v1/metrics',
)
metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# pylint: disable=C0103
app = Flask(__name__)
CORS(app)

app.register_blueprint(health_check_blueprint.create_blueprint())
app.register_blueprint(songs_blueprint.create_blueprint())

# Instrument Flask app for automatic tracing and metrics
FlaskInstrumentor().instrument_app(app)
