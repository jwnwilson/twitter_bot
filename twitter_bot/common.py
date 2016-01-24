"""
    ::Author: Noel Wilson (jwnwilson@hotmai.co.uk)

    Simple twitter application only based authentication, doesn't store the access token.
"""
import json
import pytz
import dateutil.parser
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from application_only_auth import Client
from models import Tweet
import settings

client = Client(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)


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
    :param hash_tag:
    :param start_date_time:
    :param end_data_time:
    :return:
    """
    tweets = []
    tweet_objs = []
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'
    next_url = '?q=%23'+ hash_tag + \
                '&since='+ start_date_time.strftime('%Y-%m-%d') + \
                '&until' + end_data_time.strftime('%Y-%m-%d') + \
                '&lang=en'

    while next_url:
        url = base_url + next_url
        page_data = client.request(url)
        tweets += page_data.get('statuses')
        next_url = page_data.get('search_metadata').get('next_results')

    for tweet in tweets:
        try:
            tweet_obj = Tweet.objects.get(id_str=tweet.get('id_str'))
        except ObjectDoesNotExist:
            tweet_obj  = Tweet()
            tweet_obj.id_str = tweet.get('id_str')
            tweet_obj.created_at = dateutil.parser.parse((tweet.get('created_at')))
            tweet_obj.text = tweet.get('text')
            # get the tweet typos
            get_tweet_typos(tweet_obj)
            tweet_obj.save()
        tweet_objs.append(tweet_obj)

    return tweet_objs