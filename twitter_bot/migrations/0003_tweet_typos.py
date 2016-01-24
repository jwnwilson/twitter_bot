# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_bot', '0002_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='typos',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
