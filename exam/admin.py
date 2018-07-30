# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Exam, MaterialImage, User, Score


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_type', 'material_ids')


class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class MaterialImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'name', 'account')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(MaterialImage, MaterialImageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Score)
