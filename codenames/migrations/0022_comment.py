# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-25 02:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codenames', '0021_auto_20160514_0209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time_commented', models.DateTimeField(auto_now_add=True, verbose_name=b'date started')),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('game', models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='codenames.Game')),
            ],
        ),
    ]
