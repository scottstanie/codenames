# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='color',
        ),
        migrations.AddField(
            model_name='card',
            name='colors',
            field=models.SmallIntegerField(choices=[(0, b'Red'), (1, b'Blue'), (2, b'Grey'), (3, b'Black')], default=2),
        ),
    ]
