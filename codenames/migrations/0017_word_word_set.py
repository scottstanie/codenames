# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-14 01:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0016_remove_game_current_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='word_set',
            field=models.CharField(default=b'alternate', max_length=200),
        ),
    ]
