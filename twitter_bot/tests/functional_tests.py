import os, sys
import unittest
import logging
import time
from datetime import datetime
from django.test import LiveServerTestCase
from twitter_bot.models import HashTag
from twitter_bot.models import HashTagBattle
from twitter_bot.common import get_hash_tag_typos
from twitter_bot.common import get_tweets_by_hash_tag
from twitter_bot.common import get_tweet_typos
from twitter_bot.common import get_hash_tag_most_typos


class CCViewsTestCase(LiveServerTestCase):
    fixtures = ['initial_data.json',]

    def setUp(self):
        self.url = self.live_server_url

    def tearDown(self):
        pass

    def test_create_hash_tag_battle(self):
        """
        Create hash tag battle objects in the database
        :return:
        """
        hash_tag_name_1 = "dogs"
        hash_tag_name_2 = "cats"

        hash_tag_1 = HashTag.objects.get(hash_tag=hash_tag_name_1)
        hash_tag_2 = HashTag.objects.get(hash_tag=hash_tag_name_2)
        hash_tag_battle = HashTagBattle.objects.get(hash_tags__hash_tag__in=[hash_tag_1,hash_tag_2])

        self.assertTrue(hash_tag_battle,)

    def test_get_hash_tag_tweets_between_times(self):
        """
        Get tweets from twitter api with hashtag between start and end date
        :return:
        """
        hash_tag = "dogs"
        start_date = datetime.date()
        end_date = datetime.date()
        tweets = get_tweets_by_hash_tag(hash_tag, start_date, end_date)

        self.assertEqual(len(tweets), 0)

    def test_get_typos_in_tweet(self):
        """
        Get typos in a string
        :return:
        """
        test_message = "cat dog thn that hat kool"
        typos = get_tweet_typos(test_message)

        self.assertEqual(len(typos), 2)

    def test_get_hash_tag_battle_results(self):
        """
        Check that hash tag battle returns expected results
        :return:
        """
        hash_tag = "dogs"
        start_date = datetime.date()
        end_date = datetime.date()
        typos = get_hash_tag_most_typos(hash_tag, start_date, end_date)

        self.assertEqual(len(typos), 0)

    def test_get_hash_tag_typos(self):
        """
        Check that hash tag battle returns expected results
        :return:
        """
        hash_tag_name_1 = "dogs"
        hash_tag_name_2 = "cats"

        hash_tag_1 = HashTag.objects.get(hash_tag=hash_tag_name_1)
        hash_tag_2 = HashTag.objects.get(hash_tag=hash_tag_name_2)
        hash_tag_battle = HashTagBattle.objects.get(hash_tags__hash_tag__in=[hash_tag_1,hash_tag_2])

        typos = get_hash_tag_typos(hash_tag_battle)

        self.assertEqual(len(typos), 0)

if __name__ == "__main__":
    unittest.main()