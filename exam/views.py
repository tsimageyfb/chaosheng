# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from questionnaire import http
import json, datetime, time
from .models import Exam, Question, MaterialImage


def index(request):
    # exam
    exam = Exam.objects.get(id=1)

    # questions
    questions = []
    materials = {}
    question_ids = exam.questions.split(",")
    if len(question_ids) > 0:
        questions = Question.objects.filter(id__in=question_ids)
        for question in questions:
            materials[question.id] = question.answer_options.split(",")

    # images

    context = {"exam": exam, "questions": questions, "materials": materials}
    return render(request, 'exam/index.html', context)
