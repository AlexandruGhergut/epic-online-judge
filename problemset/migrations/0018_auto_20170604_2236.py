# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0017_testcase_output'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(to='problemset.Tag'),
        ),
    ]
