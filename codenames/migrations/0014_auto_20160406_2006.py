# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codenames', '0013_auto_20160406_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guess',
            name='card',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='codenames.Card'),
        ),
    ]