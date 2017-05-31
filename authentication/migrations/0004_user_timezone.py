# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-31 06:48
from __future__ import unicode_literals

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20170421_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default='Europe/London'),
        ),
    ]
