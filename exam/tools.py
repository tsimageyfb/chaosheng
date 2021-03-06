# -*- coding: utf-8 -*-
from .models import Exam, Question, User, Score, QuestionStatistics
import json
import operator

ACCOUNT_ROBOT = 'robot'

ACCOUNT_TEAMS = ['BEIJING1', 'BEIJING2', 'SHANGHAI', 'LIAONING', 'GUANGZHOU', 'SICHUAN', 'HUBEI', 'SHANXI1',
                 'SHENZHEN', 'NEIMENG', 'HEILONGJIANG', 'SHANXI2']
NAME_TEAMS = {'BEIJING1': '北京1队', 'BEIJING2': '北京2队', 'SHANGHAI': '上海队', 'LIAONING': '辽宁队',
              'GUANGZHOU': '广州队', 'SICHUAN': '四川队', 'HUBEI': '湖北队', 'SHANXI1': '陕西队', 'SHENZHEN': '深圳队',
              'NEIMENG': '内蒙队', 'HEILONGJIANG': '黑龙江队', 'SHANXI2': '山西队'}

AUDIENCE_TYPE = [1, 2]
AUDIENCE_NAME = {1: "场内观众", 2: "场外观众"}
AUDIENCE_KEY = {1: "inner", 2: "outer"}


def get_pre_exam_winner(exam_id):
    if int(exam_id) != 2 and int(exam_id) != 3:
        # 非半决赛、决赛，都没有累加分
        return ACCOUNT_TEAMS

    pre_exam_id = 0
    count = 0
    # 半决赛
    if int(exam_id) == 2:
        pre_exam_id = 1
        count = 6
    # 决赛
    if int(exam_id) == 3:
        pre_exam_id = 2
        count = 2

    teams = []
    winner_teams = []
    for account in ACCOUNT_TEAMS:
        team_user = get_team_user(account)
        team_sore = Score.objects.filter(exam_id=pre_exam_id, user_id=team_user.id)
        if len(team_sore) > 0:
            team_sore = team_sore[0]
            teams.append({"name": NAME_TEAMS[account], "account": account, "score": team_sore.score})
    if len(teams) == 0:
        return ACCOUNT_TEAMS

    teams = sorted(teams, key=operator.itemgetter('score'), reverse=True)
    for i in range(0, count):
        if len(teams) > i:
            winner_teams.append(teams[i]['account'])

    return winner_teams


def get_pre_exam_score(exam_id, account, user_id):
    if int(exam_id) != 2 and int(exam_id) != 3:
        # 非半决赛、决赛，都没有累加分
        return 0

    pre_exam_id = 0
    # 半决赛
    if int(exam_id) == 2:
        pre_exam_id = 1
    # 决赛
    if int(exam_id) == 3:
        pre_exam_id = 2

    if account is not None and account != "":
        if account == ACCOUNT_ROBOT:
            user = get_robot_user()
        else:
            user = get_team_user(account)
    else:
        user = User.objects.get(id=user_id)

    # get pre exam score
    pre_exam_score = Score.objects.filter(exam_id=pre_exam_id, user_id=user.id)
    if len(pre_exam_score) > 0:
        pre_exam_score = pre_exam_score[0]
        return pre_exam_score.score
    # 有一种可能：没参加半决赛但初赛有成绩
    if int(exam_id) == 3:
        pre_exam_score = Score.objects.filter(exam_id=1, user_id=user.id)
        if len(pre_exam_score) > 0:
            pre_exam_score = pre_exam_score[0]
            return pre_exam_score.score
    return 0


def compute_score(exam_id, answers_dic):
    exam = Exam.objects.get(id=exam_id)
    question_ids = exam.questions.split(",")
    answers_right = {}
    score = 0

    index = 1
    for qid in question_ids:
        question = Question.objects.get(id=qid)
        answers_right[str(index)] = question.correct_answer
        index += 1

    for key, val in answers_dic.items():
        if key in answers_right:
            if answers_right[key] == val:
                score += 1
            else:
                # count wrong statistics
                qid = question_ids[int(key)-1]
                data = QuestionStatistics.objects.filter(question_id=qid)
                if data is None or len(data) == 0:
                    QuestionStatistics.objects.create(question_id=qid, wrong_count=1, user_type=0)
                else:
                    data = data[0]
                    data.wrong_count += 1
                    data.save()
    return score


def compute_answer(exam_id, answers_dic):
    exam = Exam.objects.get(id=exam_id)
    question_ids = exam.questions.split(",")
    answers_right = []
    stat = []

    for qid in question_ids:
        question = Question.objects.get(id=qid)
        answers_right.append(question.correct_answer)

    for i in range(1, len(answers_right)+1):
        if str(i) in answers_dic:
            if answers_dic[str(i)] == answers_right[i-1]:
                stat.append(1)
            else:
                stat.append(2)
        else:
            stat.append(0)
    return stat


def get_robot_user():
    robot_user = User.objects.filter(account=ACCOUNT_ROBOT)
    if len(robot_user) == 0:
        robot_user = User.objects.create(account=ACCOUNT_ROBOT)
    else:
        robot_user = robot_user[0]
    return robot_user


def get_each_team_progress(exam_id, account):
    team_user = get_team_user(account)
    team_score = Score.objects.filter(exam_id=exam_id, user_id=team_user.id)
    progress = 0

    if len(team_score) == 0:
        is_submit = False
        used_seconds = 0
    else:
        team_score = team_score[0]
        is_submit = team_score.submitted
        used_seconds = team_score.elapsed_seconds
        answer = team_score.answer
        if answer != '':
            answer_map = json.loads(answer)
            progress = len(answer_map)

    return {'id': team_user.id, 'name': NAME_TEAMS[account], 'pinyin': account, 'progress': progress,
            'is_submit': is_submit, 'used_seconds': used_seconds}


def get_team_user(account):
    team_user = User.objects.filter(account=account)
    if len(team_user) == 0:
        team_user = User.objects.create(account=account)
    else:
        team_user = team_user[0]
    return team_user


def get_audience_progress(exam_id, audience_type):
    users = User.objects.filter(user_type=audience_type)
    user_ids = []
    if len(users) > 0:
        for user in users:
            user_ids.append(user.id)
    submit = len(Score.objects.filter(exam_id=exam_id, user_id__in=user_ids))

    return {'name': AUDIENCE_NAME[audience_type], 'total': len(users), 'submit': submit}


def get_audience_rank(exam_id, count, audience_type):
    result = []
    # get users
    users = User.objects.filter(user_type=audience_type)
    map_user = {}
    for u in users:
        map_user[u.id] = u

    if len(users) == 0:
        return result
    user_ids = map(lambda each: each.id, users)
    scores = Score.objects.filter(exam_id=exam_id, user_id__in=user_ids)
    if len(scores) == 0:
        return result

    scores = sorted(scores, key=lambda each: each.score, reverse=True)
    for i in range(count):
        if len(scores) > i:
            score = scores[i]
            result.append({'name': map_user[score.user_id].name, 'order': i+1,
                           'phone': map_user[score.user_id].phone[-4:], 'score': score.score,
                           'come_from': map_user[score.user_id].prov_city+map_user[score.user_id].work_place,
                           'phone_full': map_user[score.user_id].phone, 'user_id': map_user[score.user_id].id})
    return result
