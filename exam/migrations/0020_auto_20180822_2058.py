# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-22 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0019_auto_20180820_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='work_place_level',
            field=models.CharField(blank=True, default='', max_length=24),
        ),
        migrations.AddField(
            model_name='user',
            name='work_year',
            field=models.CharField(blank=True, default='', max_length=24),
        ),
    ]