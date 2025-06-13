FROM python:3.13.5-alpine

RUN apk add --no-cache --update git make gcc python3-dev musl-dev

WORKDIR /app
COPY pyproject.toml .
COPY app app/

# Install dependencies globally
RUN pip install -e ".[dev]"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# OpenTelemetry Configuration
ENV OTEL_SERVICE_NAME=lastfm-last-played
ENV OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
ENV OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io"

# Run with debug logging and OpenTelemetry instrumentation
CMD exec opentelemetry-instrument gunicorn --pythonpath /app app.main:app --bind 0.0.0.0:${PORT:-8080} --log-level debug
