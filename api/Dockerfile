FROM python:3.12.4-alpine

RUN apk add --no-cache --update git make gcc python3-dev musl-dev

WORKDIR /app
COPY pyproject.toml .
COPY app app/

# Install dependencies globally
RUN pip install -e ".[dev]"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run with debug logging
CMD exec gunicorn --pythonpath /app app.main:app --bind 0.0.0.0:${PORT:-8080} --log-level debug
