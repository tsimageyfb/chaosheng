# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from questionnaire import http
import json
from .models import Exam, Question, MaterialImage, User, Score
from .tools import compute_score, get_robot_user, get_each_team_progress, get_team_user, ACCOUNT_TEAMS
from .tools import AUDIENCE_KEY, AUDIENCE_TYPE, get_audience_rank, get_audience_progress, NAME_TEAMS


def entry(request):
    context = {"exam_id": 1}
    return render(request, 'exam/entry.html', context)


def index(request):
    # params
    user_id = request.GET.get('user', '0')
    account = request.GET.get('account', '')
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

    context = {"exam": exam, "questions": questions, "materials": materials, "user": user_id, "account": account,
               "exam_id": exam_id}
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


@csrf_exempt
def robot_tick_answer(request):
    exam_id = request.POST['exam']
    question_id = request.POST['question']
    this_answer = request.POST['answer']

    answer_dic = {question_id: this_answer}
    answer = json.dumps(answer_dic)

    robot_user = get_robot_user()
    robot_score = Score.objects.filter(exam_id=exam_id, user_id=robot_user.id)
    if len(robot_score) == 0:
        Score.objects.create(exam_id=exam_id, user_id=robot_user.id, answer=answer)
    else:
        robot_score = robot_score[0]
        answer_new_dic = {}
        if robot_score.answer != '':
            answer_new_dic.update(json.loads(robot_score.answer))
        answer_new_dic.update(answer_dic)
        robot_score.answer = json.dumps(answer_new_dic)
        robot_score.save()

    return http.wrap_ok_response(json.loads(robot_score.answer))


@csrf_exempt
def robot_submit_answer(request):
    exam_id = request.POST['exam']

    robot_user = get_robot_user()
    robot_score = Score.objects.filter(exam_id=exam_id, user_id=robot_user.id)
    if len(robot_score) == 0:
        return http.wrap_bad_response(-1, 'not found this exam')
    else:
        robot_score = robot_score[0]
        robot_score.submitted = True
        # count score
        if robot_score.answer == '':
            point = 0
        else:
            point = compute_score(exam_id, json.loads(robot_score.answer))

        robot_score.score = point
        robot_score.save()

    return http.wrap_ok_response({"score": point})


@csrf_exempt
def robot_get_progress(request):
    exam_id = request.GET['exam']
    robot_user = get_robot_user()
    robot_score = Score.objects.filter(exam_id=exam_id, user_id=robot_user.id)
    if len(robot_score) == 0:
        return http.wrap_ok_response({})
    else:
        robot_score = robot_score[0]
        answer = "{}"
        if robot_score.answer != '':
            answer = robot_score.answer
        return http.wrap_ok_response(json.loads(answer))


@csrf_exempt
def team_get_progress(request):
    exam_id = request.GET['exam']
    progress = []
    for account in ACCOUNT_TEAMS:
        each_progress = get_each_team_progress(exam_id, account)
        progress.append(each_progress)
    return http.wrap_ok_response(progress)


@csrf_exempt
def team_get_rank(request):
    exam_id = request.GET['exam']
    rank = []
    rank.append({"name": "机器人", "order": 1, "score": 50})
    i = 0
    for account in ACCOUNT_TEAMS:
        rank.append({"name": NAME_TEAMS[account], "order": i+2, "score": 50-i-1})
        i += 1
    return http.wrap_ok_response(rank)


@csrf_exempt
def rest_seconds(request):
    exam_id = request.GET['exam']
    return http.wrap_ok_response({"rest": 600})


@csrf_exempt
def audience_get_progress(request):
    exam_id = request.GET['exam']
    progress = {}
    for aud_type in AUDIENCE_TYPE:
        progress[AUDIENCE_KEY[aud_type]] = get_audience_progress(exam_id, aud_type)
    return http.wrap_ok_response(progress)


@csrf_exempt
def audience_get_rank(request):
    exam_id = request.GET['exam']
    count = request.GET['count']
    rank = {}
    for aud_type in AUDIENCE_TYPE:
        rank[AUDIENCE_KEY[aud_type]] = get_audience_rank(exam_id, int(count), aud_type)
    return http.wrap_ok_response(rank)


@csrf_exempt
def team_tick_answer(request):
    exam_id = request.POST['exam']
    question_id = request.POST['question']
    this_answer = request.POST['answer']
    account = request.POST['account']

    answer_dic = {question_id: this_answer}
    answer = json.dumps(answer_dic)

    team_user = get_team_user(account)
    team_score = Score.objects.filter(exam_id=exam_id, user_id=team_user.id)
    if len(team_score) == 0:
        Score.objects.create(exam_id=exam_id, user_id=team_user.id, answer=answer)
    else:
        team_score = team_score[0]
        answer_new_dic = {}
        if team_score.answer != '':
            answer_new_dic.update(json.loads(team_score.answer))
        answer_new_dic.update(answer_dic)
        team_score.answer = json.dumps(answer_new_dic)
        team_score.save()

    return http.wrap_ok_response(json.loads(team_score.answer))
