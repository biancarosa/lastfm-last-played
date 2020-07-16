![build-api](https://github.com/biancarosa/lastfm-last-played/workflows/build-api/badge.svg)
![deploy-api](https://github.com/biancarosa/lastfm-last-played/workflows/deploy-api/badge.svg)

# Last.fm Last Played Songs

# Running the app

## Docker

[Docker](https://www.docker.com/) and [Docker Compose](https://www.docker.com/) make things easy!

```sh
docker-compose up
# or if you want to run detached
docker-compose up -d
```

## Natively

### The API

There is a comprehensive `Makefile` in the project that can be used.

```sh
# install dependencies
make
# runs the app
make run
# other commands
make lint
make test
make integration-test
make coverage
```
