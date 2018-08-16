# -*- coding: utf-8 -*-

from .models import Stage
import time

map_stage = {0: "模拟赛前", 1: "模拟赛开始", 2: "模拟赛结束", 3: "初赛开始", 4: "初赛结束", 5: "半决赛开始", 6: "半决赛结束",
             7: "决赛开始", 8: "决赛结束"}


def get_stage():
    stage = Stage.objects.get(id=1)
    return stage.stage


def get_stage_begin_timestamp():
    stage = Stage.objects.get(id=1)
    return stage.begin_timestamp


def set_stage(stage_obj):
    stage = Stage.objects.get(id=1)
    stage.stage = int(stage_obj)
    stage.begin_timestamp = time.time()
    stage.save()


def get_stage_name(stage):
    return map_stage[stage]