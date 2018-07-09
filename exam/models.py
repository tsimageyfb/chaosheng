# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    # 1-单选
    question_type = models.IntegerField()
    description = models.CharField(max_length=128)
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
    description = models.CharField(max_length=128)
    # 题目列表，半角逗号隔开
    questions = models.CharField(max_length=512)
    # 答题限时-秒数
    time_limit = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class MaterialImage(models.Model):
    name = models.CharField(max_length=24)
    description = models.CharField(max_length=64)
    image = models.ImageField(upload_to='material_img')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
