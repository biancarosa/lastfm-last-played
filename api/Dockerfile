FROM python:3.8.3-alpine

RUN apk add --no-cache --update git make gcc python3-dev musl-dev && \
    set -ex && \
    pip install --no-cache-dir pipenv==10.1.2

ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock

RUN set -ex && \
    pipenv install --dev --system --deploy

WORKDIR /app
ADD app .

CMD exec gunicorn app.main:app