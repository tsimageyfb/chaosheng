# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-09 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_auto_20180709_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='description',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time_limit',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(blank=True, default='', max_length=24),
        ),
        migrations.AlterField(
            model_name='materialimage',
            name='description',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='materialimage',
            name='name',
            field=models.CharField(blank=True, default='', max_length=24),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]
