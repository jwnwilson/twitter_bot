# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_tag', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HashTagBattle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('hash_tags', models.ManyToManyField(to='twitter_bot.HashTag')),
            ],
        ),
        migrations.CreateModel(
            name='HashTagBattleResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('battle_data', models.TextField()),
                ('hash_tag_battle', models.ForeignKey(to='twitter_bot.HashTagBattle')),
                ('winner', models.ForeignKey(to='twitter_bot.HashTag', null=True)),
            ],
        ),
    ]
