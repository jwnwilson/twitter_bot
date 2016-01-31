from __future__ import absolute_import

from datetime import datetime
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(run_every=datetime.timedelta(minutes=5))
def poll_twitter():
    """
    This will poll twitter for all hashtags we have stored and store all hashtags found so we can return
    tweets
    :return:
    """
    pass


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)