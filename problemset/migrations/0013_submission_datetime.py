# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-31 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0012_auto_20170530_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
