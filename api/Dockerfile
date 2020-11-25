FROM python:3.9.0-alpine

RUN apk add --no-cache --update git make gcc python3-dev musl-dev && \
    set -ex && \
    pip install --no-cache-dir pipenv==10.1.2

ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock

RUN set -ex && \
    pipenv install --dev --system --deploy

ADD app app

CMD exec gunicorn app.main:app