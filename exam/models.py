# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    # 1-单选
    question_type = models.IntegerField()
    description = models.CharField(max_length=128, default='', blank=True)
    # 选择题的各选项，半角逗号隔开
    answer_options = models.CharField(max_length=64)
    # 1-材料纯图片
    material_type = models.IntegerField()
    # 材料列表，半角逗号隔开
    material_ids = models.CharField(max_length=64)
    # 正确答案，半角逗号隔开
    correct_answer = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Exam(models.Model):
    title = models.CharField(max_length=24)
    description = models.CharField(max_length=128, default='', blank=True)
    # 题目列表，半角逗号隔开
    questions = models.CharField(max_length=512)
    # 答题限时-秒数
    time_limit = models.IntegerField(default=0, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class MaterialImage(models.Model):
    name = models.CharField(max_length=24, default='', blank=True)
    description = models.CharField(max_length=64, default='', blank=True)
    image = models.ImageField(upload_to='material_img')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class User(models.Model):
    name = models.CharField(max_length=24, default='', blank=True)
    account = models.CharField(max_length=24, default='', blank=True)
    user_type = models.IntegerField(default=0)  # 0-各代表队，1-场内观众，2-场外观众
    phone = models.CharField(max_length=18, default='', blank=True)
    address = models.CharField(max_length=128, default='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Score(models.Model):
    exam_id = models.IntegerField()
    user_id = models.IntegerField()
    answer = models.CharField(max_length=128, default='', blank=True)
    score = models.IntegerField()
    elapsed_seconds = models.IntegerField(default=0, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
