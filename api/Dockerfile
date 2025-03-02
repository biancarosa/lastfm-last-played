FROM python:3.12.4-alpine

RUN apk add --no-cache --update git make gcc python3-dev musl-dev && \
    set -ex && \
    pip install --no-cache-dir uv

WORKDIR /app
ADD pyproject.toml pyproject.toml
ADD app app

RUN set -ex && \
    uv venv && \
    uv pip install -e ".[dev]"

CMD exec gunicorn app.main:app
