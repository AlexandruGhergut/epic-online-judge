# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-02 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0013_submission_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.IntegerField(choices=[(0, 'C++'), (1, 'Python')]),
        ),
    ]