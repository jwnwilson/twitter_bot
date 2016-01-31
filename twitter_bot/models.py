from django.db import models


class HashTag(models.Model):
    """
    Store hash tags that we want to use in battles
    """
    hash_tag = models.CharField(blank=False, unique=True, max_length=100)


class Tweet(models.Model):
    """
    For each hash tag we will be storing tweets for each battle as the twitter API only goes back a week
    """
    id_str = models.CharField(blank=False, unique=True, max_length=100)
    # This can be limited later but for now to fit all unicode characters
    text = models.TextField()
    typos = models.TextField()
    created_at = models.DateTimeField(null=False)
    hash_tag = models.ForeignKey(HashTag)


class HashTagBattle(models.Model):
    """
    Store hash tag battles with a Many to Many relationship to tags we wish to include in the battle
    """
    # Add name for each battle
    name = models.CharField(unique=True, blank=False, max_length=100)
    hash_tags = models.ManyToManyField(HashTag)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()


class HashTagBattleResult(models.Model):
    """
    Store hash tag battles with a Many to Many relationship to tags we wish to include in the battle
    """
    # Add name for each battle
    hash_tag_battle = models.ForeignKey(HashTagBattle)
    winner = models.ForeignKey(HashTag, null=True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    battle_data = models.TextField()