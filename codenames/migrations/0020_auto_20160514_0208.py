# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-14 02:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0019_wordset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='word_set',
        ),
        migrations.RemoveField(
            model_name='word',
            name='word_set',
        ),
    ]
