# -*- coding: utf-8 -*-

from .models import Stage
import time


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
