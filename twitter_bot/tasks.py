from __future__ import absolute_import

import datetime
import logging
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .models import HashTag
from .common import get_tweets_data_for_hash_tag_from_twitter

logger = logging.getLogger(__name__)


@periodic_task(run_every=datetime.timedelta(hours=1))
def poll_twitter():
    """
    This will poll twitter for all hashtags we have stored and store all hashtags found so we can return
    tweets
    :return:
    """
    logger.info("Starting twitter poll")
    for hash_tag in HashTag.objects.all():
        logger.info("Polling for hashtag: %s" % hash_tag.hash_tag)
        get_tweets_data_for_hash_tag_from_twitter(hash_tag.hash_tag)
    logger.info("Twitter poll complete")


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)