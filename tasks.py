import os

from celery import Celery
from celery.schedules import crontab

from google_news.headlines import Headlines

ONE_HOUR = 3600  # in seconds
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'pyamqp://guest@localhost//')
APP = Celery(broker=RABBITMQ_URL)


@APP.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Call collect_google_news() every hour.
    """
    sender.add_periodic_task(
        ONE_HOUR, collect_google_news.s(), expires=ONE_HOUR / 2)


@APP.task
def collect_google_news():
    headlines = Headlines()
    headlines.store()
