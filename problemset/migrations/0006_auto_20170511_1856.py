# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-11 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0005_auto_20170510_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]
