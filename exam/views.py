# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from questionnaire import http
import json, datetime, time
from .models import Exam, Question, MaterialImage, User


def entry(request):
    context = {}
    return render(request, 'exam/entry.html', context)


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
            materials[question.id] = {"options": question.answer_options.split(",")}
            # images
            image_ids = question.material_ids.split(",")
            image_objs = MaterialImage.objects.filter(id__in=image_ids)
            images = []
            for image in image_objs:
                images.append(image.image)
            materials[question.id].update({"images": images})
    #

    context = {"exam": exam, "questions": questions, "materials": materials}
    return render(request, 'exam/index.html', context)


def score(request):
    context = {}
    return render(request, 'exam/score.html', context)


@csrf_exempt
def ajax_create_user(request):
    phone = request.POST['phone']
    user_type = request.POST['user_type']
    address = request.POST['address']

    ob = User.objects.create(phone=phone, user_type=user_type, address=address)
    return HttpResponse(ob.id)
