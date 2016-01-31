# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_bot', '0003_tweet_typos'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='hash_tag',
            field=models.ForeignKey(default=1, to='twitter_bot.HashTag'),
            preserve_default=False,
        ),
    ]
