from django.db import models


class HashTag(models.Model):
    """
    Store hash tags that we want to use in battles
    """
    hash_tag = models.CharField(blank=False, unique=True, max_length=100)


class HashTagBattle(models.Model):
    """
    Store hash tag battles with a Many to Many relationship to tags we wish to include in the battle
    """
    # Add name for each battle
    name = models.CharField(unique=True, blank=False, max_length=100)
    hash_tags = models.ManyToManyField(HashTag)
    start_data = models.DateTimeField()
    end_data = models.DateTimeField()


class HashTagBattleResults(models.Model):
    """
    Store hash tag battles with a Many to Many relationship to tags we wish to include in the battle
    """
    # Add name for each battle
    hash_tag_battle = models.ForeignKey(HashTagBattle)
    winner = models.ForeignKey(HashTag, null=True)
    start_data = models.DateTimeField()
    end_data = models.DateTimeField()
    battle_data = models.TextField()