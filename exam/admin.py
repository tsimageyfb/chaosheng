# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Exam, MaterialImage, User, Score, MaterialVideo, QuestionStatistics, Stage


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_type', 'material_ids', 'correct_answer')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class MaterialImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_link', 'image')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'account', 'user_type')


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam_id', 'user_id', 'score', 'submitted', 'begin_at')


class MaterialVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_link')


class QuestionStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'wrong_count', 'user_type')


class StageAdmin(admin.ModelAdmin):
    list_display = ('id', 'stage', 'begin_timestamp')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(MaterialImage, MaterialImageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(MaterialVideo, MaterialVideoAdmin)
admin.site.register(QuestionStatistics, QuestionStatisticsAdmin)
admin.site.register(Stage, StageAdmin)
