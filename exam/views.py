# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from questionnaire import http
import json
from .models import Exam, Question, MaterialImage, User, Score, MaterialVideo, QuestionStatistics
from .tools import compute_score, get_robot_user, get_each_team_progress, get_team_user, ACCOUNT_TEAMS, ACCOUNT_ROBOT
from .tools import AUDIENCE_KEY, AUDIENCE_TYPE, get_audience_rank, get_audience_progress, NAME_TEAMS, get_pre_exam_score
from .tools import get_pre_exam_winner
import django.utils.timezone as timezone
import operator
from .stage import get_stage, get_stage_begin_timestamp, set_stage, get_stage_name
import time


def simulate_entry(request):
    # if init page, clean cache
    if get_stage() == 0:
        request.session.clear()
    context = {}
    return render(request, 'exam/simulate_entry.html', context)


def simulate_exam(request):
    user_id = request.GET['user']
    # exam
    exam = Exam.objects.get(id=4)

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
                        images.append("/statics/" + str(image.image))
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

    context = {"exam": exam, "questions": questions, "materials": materials, "exam_id": 4, "stage": get_stage(),
               "obj_stage": 1, "user_id": user_id}
    return render(request, 'exam/index.html', context)


@csrf_exempt
def ajax_post_answer_simulate(request):
    exam_id = request.POST['exam']
    answer_raw = request.POST['answer']
    answers = answer_raw.split(",")
    correct_answers = []
    exam = Exam.objects.get(id=exam_id)
    question_ids = exam.questions.split(",")
    for qid in question_ids:
        question = Question.objects.get(id=qid)
        correct_answers.append(question.correct_answer)

    answer_score = 0
    for k in range(len(answers)):
        if answers[k] == correct_answers[k]:
            answer_score += 1
    return HttpResponse(answer_score)


def entry(request):
    # if init page, clean cache
    if get_stage() == 0:
        request.session.clear()

    user_id = request.session.get('user_id', '0')
    exam_id = request.session.get('exam_id', '1')
    # stage: 1-exam, 2-score
    stage_now = request.session.get('stage', '1')
    if user_id != '0':
        check_user = User.objects.filter(id=user_id)
        if len(check_user) > 0:
            # 用户存在才跳缓存
            if stage_now == '1':
                return HttpResponseRedirect("answer?exam="+str(exam_id)+"&user="+str(user_id))
            else:
                check_score = Score.objects.filter(exam_id=exam_id, user_id=user_id)
                if len(check_score) > 0:
                    return HttpResponseRedirect("score?exam="+str(exam_id)+"&user="+str(user_id))

    user_type = request.GET.get("user_type", "inner")
    context = {"exam_id": exam_id, "user_type": user_type}
    return render(request, 'exam/entry.html', context)


def entry_team(request):
    context = {"exam_id": 1, "team": NAME_TEAMS}
    return render(request, 'exam/team.html', context)


def index(request):
    # params
    user_id = request.GET.get('user', '0')
    account = request.GET.get('account', '')
    exam_id = request.GET['exam']
    if int(exam_id) > 0 and int(exam_id) != 4:
        # 模拟卷不要写入缓存！
        request.session['exam_id'] = str(exam_id)
        request.session['stage'] = "1"

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

    # stage
    obj_stage = get_obj_stage(exam_id)

    # 判断是否要跳转
    if get_stage() > obj_stage and int(exam_id) < 3:
        if account != '':
            return HttpResponseRedirect('/exam/answer?exam='+str(int(exam_id)+1)+"&account="+account)
        elif user_id != '0':
            return HttpResponseRedirect('/exam/answer?exam='+str(int(exam_id)+1)+"&user="+user_id)

    context = {"exam": exam, "questions": questions, "materials": materials, "user_id": user_id, "account": account,
               "exam_id": exam_id, "stage": get_stage(), "obj_stage": obj_stage}
    return render(request, 'exam/index.html', context)


def get_obj_stage(exam_id):
    obj_stage = 0
    if int(exam_id) == 4:
        obj_stage = 1
    if int(exam_id) == 1:
        obj_stage = 3
    if int(exam_id) == 2:
        obj_stage = 5
    if int(exam_id) == 3:
        obj_stage = 7
    return obj_stage


def score(request):
    exam_id = request.GET.get('exam', 1)
    account = request.GET.get('account', '')
    user_id = request.GET.get('user', 0)
    score_simu = request.GET.get('score', 0)
    if exam_id != "4":
        request.session['stage'] = "2"
    if account != '':
        user = get_team_user(account)
        user_id = user.id
    ob = None
    if user_id != 0:
        ob = Score.objects.get(exam_id=exam_id, user_id=user_id)

    if ob is not None:
        count = len(ob.answer.split(","))
        right = ob.score
    else:
        count = 10
        right = score_simu
    context = {"count": count, "right": right, "exam_id": int(exam_id), "account": account, "user_id": user_id}
    return render(request, 'exam/score.html', context)


def statistics(request):
    exam_id = request.GET['exam']
    exam = Exam.objects.get(id=exam_id)
    scores = Score.objects.filter(exam_id=exam_id)

    context = {"exam": exam, "scores": scores}
    return render(request, 'exam/statistics.html', context)


@csrf_exempt
def ajax_create_user(request):
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    user_type = request.POST.get('user_type', 0)
    address = request.POST.get('address', '')
    account = request.POST.get('account', '')
    prov_city = request.POST.get('prov_city', '')
    job_title = request.POST.get('job_title', '')
    work_place = request.POST.get('work_place', '')
    work_place_level = request.POST.get('work_place_level', '')
    work_year = request.POST.get('work_year', '')
    gender = request.POST.get('gender', '')
    age = request.POST.get('age', '')

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
            user = User.objects.create(phone=phone, user_type=user_type, address=address, prov_city=prov_city,
                                       job_title=job_title, work_place=work_place, work_place_level=work_place_level,
                                       work_year=work_year, name=name, gender=gender, age=age)
        else:
            user = user[0]
            if name != '':
                user.name = name
            if user_type != 0:
                user.user_type = user_type
            if address != '':
                user.address = address
            if prov_city != '':
                user.prov_city = prov_city
            if job_title != '':
                user.job_title = job_title
            if work_place != '':
                user.work_place = work_place
            if work_place_level != '':
                user.work_place_level = work_place_level
            if work_year != '':
                user.work_year = work_year
            user.save()

        request.session['user_id'] = user.id
    return HttpResponse(user.id)


@csrf_exempt
def ajax_post_answer(request):
    user = request.POST['user']
    exam_id = request.POST['exam']
    answer_raw = request.POST['answer']
    answers = answer_raw.split(",")
    correct_answers = []
    exam = Exam.objects.get(id=exam_id)
    question_ids = exam.questions.split(",")
    for qid in question_ids:
        question = Question.objects.get(id=qid)
        correct_answers.append(question.correct_answer)

    answer_score = get_pre_exam_score(exam_id, None, user)
    # 没超时才算分
    if get_stage() == get_obj_stage(exam_id):
        for k in range(len(answers)):
            if answers[k] == correct_answers[k]:
                answer_score += 1

    # find if existed
    user_score = Score.objects.filter(exam_id=exam_id, user_id=user)
    if len(user_score) > 0:
        user_score = user_score[0]
        user_score.answer = answer_raw
        user_score.score = answer_score
        user_score.submitted = True
        user_score.save()
    else:
        user_score = Score.objects.create(exam_id=exam_id, user_id=user, answer=answer_raw,
                                          score=answer_score, submitted=True)
    # wrong rank
    map_answers = {}
    for i in range(len(answers)):
        map_answers[str(i+1)] = answers[i]
    compute_score(exam_id, map_answers)

    return HttpResponse(user_score.id)


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
        robot_score = Score.objects.create(exam_id=exam_id, user_id=robot_user.id, answer=answer)
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
        point = get_pre_exam_score(exam_id, ACCOUNT_ROBOT, 0)
        if robot_score.answer == '':
            point += 0
        else:
            point += compute_score(exam_id, json.loads(robot_score.answer))

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
    for account in get_pre_exam_winner(exam_id):
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
        elif int(exam_id) == 3:
            # 决赛要返回所有代表队成绩
            team_sore = Score.objects.filter(exam_id=2, user_id=team_user.id)
            if len(team_sore) == 0:
                team_sore = Score.objects.filter(exam_id=1, user_id=team_user.id)
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
    map_exam_stage = {4: 1, 1: 3, 2: 5, 3: 7}
    time_limit = Exam.objects.get(id=exam_id).time_limit
    rest = 0
    if get_stage() == map_exam_stage[int(exam_id)]:
        rest = time_limit - (time.time() - get_stage_begin_timestamp())
        if rest < 0:
            rest = 0

    return http.wrap_ok_response({"rest": int(rest)})


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
    count = request.GET.get('count', "10")
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
        point = get_pre_exam_score(exam_id, account, 0)
        if team_score.answer == '':
            point += 0
        else:
            point += compute_score(exam_id, json.loads(team_score.answer))

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
        explain_pics = [question.explain_image_link]
        material_ids = question.material_ids.split(",")
        if question.material_type == 1:
            materials = map(lambda each: each["image_link"], MaterialImage.objects.filter(id__in=material_ids).values("image_link"))
        if question.material_type == 2:
            materials = map(lambda each: each["video_link"], MaterialVideo.objects.filter(id__in=material_ids).values("video_link"))
        result.append({"order": i+1, "wrong_count": stat.wrong_count, "material_type": question.material_type,
                       "question_number": map_question_number[str(stat.question_id)], "materials": materials,
                       "correct_answer": int(question.correct_answer), "explain_pics": explain_pics})
        i += 1
    return http.wrap_ok_response(result)


@csrf_exempt
def show_exam(request):
    exam_id = request.GET['exam']
    exam = Exam.objects.get(id=exam_id)
    question_ids = exam.questions.split(',')
    count = 1
    questions = []
    for question_id in question_ids:
        question = {}
        question_obj = Question.objects.get(id=question_id)
        question['question_number'] = count
        question['material_type'] = question_obj.material_type
        material_ids = question_obj.material_ids.split(',')
        material_links = []
        for material_id in material_ids:
            if question_obj.material_type == 1:
                material_links.append(MaterialImage.objects.get(id=material_id).image_link)
            elif question_obj.material_type == 2:
                material_links.append(MaterialVideo.objects.get(id=material_id).video_link)
        question['material_links'] = material_links
        questions.append(question)
        count += 1

    exam_data = {'exam_id': int(exam_id), 'exam_title': exam.title, 'questions': questions}
    return http.wrap_ok_response(exam_data)


@csrf_exempt
def req_get_stage(request):
    return http.wrap_ok_response({"stage": get_stage()})


@csrf_exempt
def req_set_stage(request):
    stage_obj = request.GET['stage']
    set_stage(stage_obj)
    return http.wrap_ok_response(None)


def stage(request):
    context = {"stage": get_stage_name(get_stage())}
    return render(request, 'exam/stage.html', context)


@csrf_exempt
def add_stage(request):
    stage_now = get_stage()
    if int(stage_now) < 8:
        set_stage(int(stage_now) + 1)

    # 可能要帮助代表队提交
    stage_to = int(stage_now) + 1
    exam_id = 0
    if stage_to in [2, 4, 6, 8]:
        if stage_to == 2:
            exam_id = 4
        if stage_to == 4:
            exam_id = 1
        if stage_to == 6:
            exam_id = 2
        if stage_to == 8:
            exam_id = 3
    scores = Score.objects.filter(exam_id=exam_id, submitted=False)
    if len(scores) > 0:
        for each in scores:
            each.submitted = True
            user = User.objects.get(id=each.user_id)
            # count score
            point = get_pre_exam_score(exam_id, user.account, 0)
            if each.answer == '':
                point += 0
            else:
                point += compute_score(exam_id, json.loads(each.answer))

            each.elapsed_seconds = int((timezone.now() - each.begin_at).total_seconds())
            each.score = point
            each.save()

    return HttpResponse("ok")


@csrf_exempt
def sub_stage(request):
    stage_now = get_stage()
    if int(stage_now) > 0:
        set_stage(int(stage_now) - 1)
    return HttpResponse("ok")
