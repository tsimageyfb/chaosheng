# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-09 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='description',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time_limit',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='materialimage',
            name='description',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='materialimage',
            name='name',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
