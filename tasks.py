import os

from celery import Celery
from celery.schedules import crontab

from google_news.headlines import Headlines

ONE_HOUR = 3600  # in seconds
TASK_PERIODICITY_IN_HOURS = os.environ.get('GNEWS_TASK_PERIODICITY', '1')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'pyamqp://guest@localhost//')
APP = Celery(broker=RABBITMQ_URL)


@APP.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Call collect_google_news() every hour.
    """
    task_periodicity = round(ONE_HOUR * float(TASK_PERIODICITY_IN_HOURS))
    sender.add_periodic_task(
        task_periodicity, collect_google_news.s(), expires=task_periodicity / 2)


@APP.task
def collect_google_news():
    headlines = Headlines()
    headlines.store()
