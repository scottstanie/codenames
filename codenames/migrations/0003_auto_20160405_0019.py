# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-05 00:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0002_auto_20160404_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='colors',
            new_name='color',
        ),
    ]
