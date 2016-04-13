# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 21:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codenames', '0014_auto_20160406_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='current_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='current_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
