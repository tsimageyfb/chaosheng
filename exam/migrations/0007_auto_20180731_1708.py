# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-31 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_score_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_options',
            field=models.CharField(default='\u6b63\u5e38,\u826f\u6027,\u6076\u6027', max_length=64),
        ),
        migrations.AlterField(
            model_name='question',
            name='material_type',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.IntegerField(default='1'),
        ),
    ]
