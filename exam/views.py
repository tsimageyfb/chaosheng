# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from questionnaire import http
import json, datetime, time
from .models import Exam, Question, MaterialImage, User, Score


def entry(request):
    context = {"exam_id": 1}
    return render(request, 'exam/entry.html', context)


def index(request):
    # params
    user_id = request.GET['user']
    exam_id = request.GET['exam']

    # exam
    exam = Exam.objects.get(id=exam_id)

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

    context = {"exam": exam, "questions": questions, "materials": materials, "user": user_id, "exam_id": exam_id}
    return render(request, 'exam/index.html', context)


def score(request):
    score_id = request.GET['id']
    ob = Score.objects.get(id=score_id)
    count = 0
    right = 0
    if ob is not None:
        count = len(ob.answer.split(","))
        right = ob.score
    context = {"count": count, "right": right}
    return render(request, 'exam/score.html', context)


def statistics(request):
    exam_id = request.GET['exam']
    exam = Exam.objects.get(id=exam_id)
    scores = Score.objects.filter(exam_id=exam_id)

    context = {"exam": exam, "scores": scores}
    return render(request, 'exam/statistics.html', context)


@csrf_exempt
def ajax_create_user(request):
    phone = request.POST['phone']
    user_type = request.POST['user_type']
    address = request.POST['address']

    ob = User.objects.create(phone=phone, user_type=user_type, address=address)
    return HttpResponse(ob.id)


@csrf_exempt
def ajax_post_answer(request):
    user = request.POST['user']
    exam_id = request.POST['exam']
    answer_raw = request.POST['answer']
    answers = answer_raw.split(",")
    correct_answers = []
    exam = Exam.objects.get(id=1)
    question_ids = exam.questions.split(",")
    for qid in question_ids:
        question = Question.objects.get(id=qid)
        correct_answers.append(question.correct_answer)

    answer_score = 0
    for k in range(len(answers)):
        if answers[k] == correct_answers[k]:
            answer_score += 1

    ob = Score.objects.create(exam_id=exam_id, user_id=user, answer=answer_raw, score=answer_score)
    return HttpResponse(ob.id)
