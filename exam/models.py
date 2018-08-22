# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Question(models.Model):
    # 1-单选
    question_type = models.IntegerField(default='1')
    description = models.CharField(max_length=128, default='', blank=True)
    # 选择题的各选项，半角逗号隔开
    answer_options = models.CharField(max_length=64, default='良性,恶性')
    # 1-材料纯图片, 2-材料纯视频
    material_type = models.IntegerField(default='1')
    # 材料列表，半角逗号隔开
    material_ids = models.CharField(max_length=64)
    # 正确答案，半角逗号隔开
    correct_answer = models.CharField(max_length=64)
    # 解析图片
    explain_image_link = models.CharField(max_length=256, default='', blank=True)

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
    image = models.ImageField(upload_to='material_img', blank=True)
    image_link = models.CharField(max_length=256, default='', blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class User(models.Model):
    name = models.CharField(max_length=24, default='', blank=True)
    account = models.CharField(max_length=24, default='', blank=True)
    user_type = models.IntegerField(default=0)  # 0-各代表队和robot，1-场内观众，2-场外观众
    phone = models.CharField(max_length=18, default='', blank=True)
    address = models.CharField(max_length=128, default='', blank=True)

    prov_city = models.CharField(max_length=64, default='', blank=True)  # 省市
    work_place = models.CharField(max_length=128, default='', blank=True)  # 工作单位
    job_title = models.CharField(max_length=32, default='', blank=True)  # 职称
    work_place_level = models.CharField(max_length=24, default='', blank=True)  # 医院等级
    work_year = models.CharField(max_length=24, default='', blank=True)  # 工作年限

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Score(models.Model):
    exam_id = models.IntegerField()
    user_id = models.IntegerField()
    answer = models.CharField(max_length=512, default='', blank=True)
    score = models.IntegerField(default=0, blank=True)
    begin_at = models.DateTimeField(auto_now_add=True, editable=True)
    elapsed_seconds = models.IntegerField(default=0, blank=True)
    submitted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class MaterialVideo(models.Model):
    name = models.CharField(max_length=24, default='', blank=True)
    description = models.CharField(max_length=64, default='', blank=True)
    video_link = models.CharField(max_length=256, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class QuestionStatistics(models.Model):
    question_id = models.IntegerField()
    wrong_count = models.IntegerField(default=0)
    user_type = models.IntegerField(default=0)  # 0-各代表队和robot，1-场内观众，2-场外观众

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Stage(models.Model):
    # 阶段：0-模拟赛前，1-模拟赛开始，2-模拟赛结束，3-初赛开始，4-初赛结束，5-半决赛开始，6-半决赛结束，7-决赛开始，8-决赛结束
    stage = models.IntegerField()
    begin_timestamp = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
