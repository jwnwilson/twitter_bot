"""
    ::Author: Noel Wilson (jwnwilson@hotmai.co.uk)

    Simple twitter application only based authentication, doesn't store the access token.
"""
import json
import pytz
import logging
import dateutil.parser
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from application_only_auth import Client
from models import Tweet
from models import HashTag
import settings

client = Client(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
logger = logging.getLogger(__name__)


def get_tweet_typos(tweet):
    """
    Return a list of typos found in hash_tag string
    :param hash_tags:
    :return:
    """
    typos = []
    chkr = SpellChecker("en_GB",filters=[EmailFilter,URLFilter])
    chkr.set_text(tweet.text)

    for err in chkr:
        typos.append(err.word)

    tweet.typos = json.dumps(typos)

    return typos


def get_hash_tag_most_typos(hash_tag_battle):
    """
    Return the hash tag object with the most typos
    :param hash_tag_battle:
    :return:
    """
    hash_tag_typos_data = get_hash_tag_typos(hash_tag_battle)
    most_typos = 0
    hash_tag_typos = {}
    winner = None

    for hash_tag in hash_tag_typos_data:
        hash_tag_typos[hash_tag] = 0
        for tweet in hash_tag_typos_data[hash_tag]["tweets"]:
            hash_tag_typos[hash_tag] += len(tweet["typos"])
        if hash_tag_typos[hash_tag] > most_typos:
            winner = hash_tag
            most_typos = hash_tag_typos[hash_tag]

    return winner, hash_tag_typos


def get_hash_tag_typos(hash_tag_battle):
    """
    Return the hash tag object with the most typos
    :param hash_tags:
    :return:
    """
    hash_tags = hash_tag_battle.hash_tags.all()
    hash_tags_data = {}
    for hash_tag in hash_tags:
        hash_tags_data[hash_tag] = {"tweets": []}
        tweets = get_tweets_by_hash_tag(hash_tag.hash_tag,
                                        hash_tag_battle.start_date_time,
                                        hash_tag_battle.end_date_time)

        for tweet in tweets:
            try:
                typos = json.loads(tweet.typos)
            except ValueError:
                typos = []

            tweet_obj = {'tweet':tweet.text, 'typos': typos}
            hash_tags_data[hash_tag]["tweets"].append(tweet_obj)

    return hash_tags_data


def get_tweets_by_hash_tag(hash_tag, start_date_time, end_data_time):
    """
    Get tweets by hash tag between start and end datetime
    :param hash_tag: string, hash tag to get tweets for
    :param start_date_time: datetime, get tweets with created_at older or equal to start_date_time
    :param end_data_time: datetime, get tweets with created_at before or equal to end_date_time
    :return: Queryset, tweets returned
    """
    tweets = Tweet.objects.filter(hash_tag__hash_tag=hash_tag,
                                  created_at__gte=start_date_time,
                                  created_at__lte=end_data_time)

    return tweets


def get_tweets_data_for_hash_tag_from_twitter(hash_tag):
    """
    Get tweets by hash tag data from twitter
    :param hash_tag:
    :return:
    """
    hash_tag = HashTag.objects.get(hash_tag=hash_tag)
    tweets = []
    new_tweets = 0
    tweet_objs = []
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'
    next_url = '?q=%23'+ hash_tag.hash_tag + '&lang=en'

    logger.info("Getting Tweet data for hashtag: %s" % hash_tag.hash_tag)

    while next_url:
        url = base_url + next_url
        page_data = client.request(url)
        tweets += page_data.get('statuses')
        next_url = page_data.get('search_metadata').get('next_results')

    for tweet in tweets:
        try:
            tweet_obj = Tweet.objects.get(id_str=tweet.get('id_str'))
        except ObjectDoesNotExist:
            tweet_obj = Tweet()
            tweet_obj.id_str = tweet.get('id_str')
            tweet_obj.created_at = dateutil.parser.parse((tweet.get('created_at')))
            tweet_obj.text = tweet.get('text')
            tweet_obj.hash_tag = hash_tag
            # get the tweet typos
            get_tweet_typos(tweet_obj)
            tweet_obj.save()
            new_tweets += 1
        tweet_objs.append(tweet_obj)

    logger.info("Found %s tweets for hashtag: %s" % (len(tweet_objs), hash_tag.hash_tag))
    logger.info("Found %s new tweets for hashtag: %s" % (str(new_tweets), hash_tag.hash_tag))

    return tweet_objs
