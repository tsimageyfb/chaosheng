# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Exam, MaterialImage

admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(MaterialImage)
