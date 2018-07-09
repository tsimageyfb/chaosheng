# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Exam, MaterialImage


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_type', 'material_ids')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class MaterialImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(MaterialImage, MaterialImageAdmin)
