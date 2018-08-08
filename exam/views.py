# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from questionnaire import http
import json
from .models import Exam, Question, MaterialImage, User, Score, MaterialVideo, QuestionStatistics
from .tools import compute_score, get_robot_user, get_each_team_progress, get_team_user, ACCOUNT_TEAMS, ACCOUNT_ROBOT
from .tools import AUDIENCE_KEY, AUDIENCE_TYPE, get_audience_rank, get_audience_progress, NAME_TEAMS
import django.utils.timezone as timezone
import operator


def entry(request):
    context = {"exam_id": 1}
    return render(request, 'exam/entry.html', context)


def entry_team(request):
    context = {"exam_id": 1, "team": NAME_TEAMS}
    return render(request, 'exam/team.html', context)


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
            if question.material_type == 1:
                # images
                image_ids = question.material_ids.split(",")
                image_objs = MaterialImage.objects.filter(id__in=image_ids)
                images = []
                for image in image_objs:
                    if image.image_link != "":
                        images.append(image.image_link)
                    else:
                        images.append("/statics/"+str(image.image))
                materials[question.id].update({"images": images})
            elif question.material_type == 2:
                # video
                video_ids = question.material_ids.split(",")
                video_objs = MaterialVideo.objects.filter(id__in=video_ids)
                videos = []
                for video in video_objs:
                    if video.video_link != "":
                        videos.append(video.video_link)
                materials[question.id].update({"videos": videos})

    context = {"exam": exam, "questions": questions, "materials": materials, "user": user_id, "account": account,
               "exam_id": exam_id}
    return render(request, 'exam/index.html', context)


def score(request):
    score_id = request.GET['id']
    exam_id = request.GET['exam']
    account = request.GET.get('account', '')
    ob = Score.objects.get(id=score_id)
    count = 0
    right = 0
    if ob is not None:
        count = len(ob.answer.split(","))
        right = ob.score
    context = {"count": count, "right": right, "exam_id": int(exam_id), "account": account}
    return render(request, 'exam/score.html', context)


def statistics(request):
    exam_id = request.GET['exam']
    exam = Exam.objects.get(id=exam_id)
    scores = Score.objects.filter(exam_id=exam_id)

    context = {"exam": exam, "scores": scores}
    return render(request, 'exam/statistics.html', context)


@csrf_exempt
def ajax_create_user(request):
    phone = request.POST.get('phone', '')
    user_type = request.POST.get('user_type', 0)
    address = request.POST.get('address', '')
    account = request.POST.get('account', '')

    if account != '':
        # 是代表队
        user = User.objects.filter(account=account)
        if len(user) == 0:
            user = User.objects.create(account=account, user_type=0)
        else:
            user = user[0]
    else:
        # 是观众
        user = User.objects.filter(phone=phone, user_type=user_type)
        if len(user) == 0:
            user = User.objects.create(phone=phone, user_type=user_type, address=address)
        else:
            user = user[0]
    return HttpResponse(user.id)


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
        else:
            robot_score.begin_at = timezone.now()
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

        robot_score.elapsed_seconds = int((timezone.now()-robot_score.begin_at).total_seconds())
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
    # 先找机器人
    robot_user = get_robot_user()
    robot_score = Score.objects.filter(exam_id=exam_id, user_id=robot_user.id)
    if len(robot_score) != 0:
        robot_score = robot_score[0]
        rank.append({"name": "机器人", "order": 0, "score": robot_score.score})
    # 再找代表队
    for account in ACCOUNT_TEAMS:
        team_user = get_team_user(account)
        team_sore = Score.objects.filter(exam_id=exam_id, user_id=team_user.id)
        if len(team_sore) != 0:
            team_sore = team_sore[0]
            rank.append({"name": NAME_TEAMS[account], "order": 0, "score": team_sore.score})

    # 排序
    rank = sorted(rank, key=operator.itemgetter('score'), reverse=True)
    for i in range(len(rank)):
        rank[i]['order'] = i+1
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
        team_score = Score.objects.create(exam_id=exam_id, user_id=team_user.id, answer=answer)
    else:
        team_score = team_score[0]
        answer_new_dic = {}
        if team_score.answer != '':
            answer_new_dic.update(json.loads(team_score.answer))
        else:
            team_score.begin_at = timezone.now()
        answer_new_dic.update(answer_dic)
        team_score.answer = json.dumps(answer_new_dic)
        team_score.save()

    return http.wrap_ok_response(json.loads(team_score.answer))


@csrf_exempt
def team_submit_answer(request):
    exam_id = request.POST['exam']
    account = request.POST['account']

    team_user = get_team_user(account)
    team_score = Score.objects.filter(exam_id=exam_id, user_id=team_user.id)
    if len(team_score) == 0:
        return http.wrap_bad_response(-1, 'not found this exam')
    else:
        team_score = team_score[0]
        team_score.submitted = True
        # count score
        if team_score.answer == '':
            point = 0
        else:
            point = compute_score(exam_id, json.loads(team_score.answer))

        team_score.elapsed_seconds = int((timezone.now()-team_score.begin_at).total_seconds())
        team_score.score = point
        team_score.save()

    return HttpResponse(team_score.id)


@csrf_exempt
def wrong_rank(request):
    exam_id = request.GET['exam']
    count = request.GET.get('count', 5)

    # find questions
    question_ids = Exam.objects.get(id=exam_id).questions.split(",")
    if question_ids is None or len(question_ids) == 0:
        return http.wrap_ok_response(None)

    # find statistics
    data = QuestionStatistics.objects.filter(question_id__in=question_ids).order_by("-wrong_count")
    if data is None or len(data) == 0:
        return http.wrap_ok_response(None)

    # wrap
    map_question_number = {}
    i = 1
    for qid in question_ids:
        map_question_number[qid] = i
        i += 1

    result = []
    i = 0
    for stat in data:
        if i >= count:
            return http.wrap_ok_response(result)
        # get materials
        materials = []
        question = Question.objects.get(id=stat.question_id)
        material_ids = question.material_ids.split(",")
        if question.material_type == 1:
            materials = map(lambda each: each["image_link"], MaterialImage.objects.filter(id__in=material_ids).values("image_link"))
        if question.material_type == 2:
            materials = map(lambda each: each["video_link"], MaterialVideo.objects.filter(id__in=material_ids).values("video_link"))
        result.append({"order": i+1, "wrong_count": stat.wrong_count, "material_type": question.material_type,
                       "question_number": map_question_number[str(stat.question_id)], "materials": materials,
                       "correct_answer": int(question.correct_answer)})
        i += 1
    return http.wrap_ok_response(result)
