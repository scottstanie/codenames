# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 21:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0015_game_current_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='current_user',
        ),
    ]
