# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0010_game_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
