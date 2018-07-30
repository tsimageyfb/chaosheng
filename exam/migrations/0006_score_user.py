# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-30 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20180709_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('answer', models.CharField(blank=True, default='', max_length=128)),
                ('score', models.IntegerField()),
                ('elapsed_seconds', models.IntegerField(blank=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=24)),
                ('account', models.CharField(blank=True, default='', max_length=24)),
                ('user_type', models.IntegerField(default=0)),
                ('phone', models.CharField(blank=True, default='', max_length=18)),
                ('address', models.CharField(blank=True, default='', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
