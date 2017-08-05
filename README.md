# Truth or dare?

*Automated fact checking for everyone.*

**🚧 Under development. At this time, there is nothing useful to see here. 🚧**

## Development setup

Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

```console
$ docker-compose run worker python -m unittest
```

If you see a sequence of dots, it means everything is working (at least for development).

## Running for development

```console
$ cp .env.example .env
$ docker-compose up
```

## Running in production

```console
$ export $(cat .env | xargs)
$ docker-machine create \
    --driver google \
    --google-project $GCLOUD_PROJECT \
    --google-zone $GCLOUD_ZONE \
    --engine-install-url=https://web.archive.org/web/20170623081500/https://get.docker.com \
    truth-or-dare-google
$ eval $(docker-machine env truth-or-dare-google)
$ docker-compose -f docker-compose.yml up
```