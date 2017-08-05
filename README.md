# Truth or dare?

*Automated fact checking for everyone.*

**🚧 Under development. At this time, there is nothing useful to see here. 🚧**

## Setup

Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

```console
$ docker-compose run worker python -m unittest
```

If you see a sequence of dots, it means everything is working (at least for development).

## Running

```console
$ cp .env.example .env
$ docker-compose up
```