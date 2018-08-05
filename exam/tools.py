# -*- coding: utf-8 -*-
from .models import Exam, Question, User, Score

ACCOUNT_ROBOT = 'robot'

ACCOUNT_TEAMS = ['BEIJING1', 'BEIJING2', 'SHANGHAI', 'LIAONING', 'GUANGZHOU', 'SICHUAN', 'HUBEI', 'SHANXI1',
                 'SHENZHEN', 'NEIMENG', 'HEILONGJIANG', 'SHANXI2']

NAME_TEAMS = {'BEIJING1': '北京1队', 'BEIJING2': '北京2队', 'SHANGHAI': '上海队', 'LIAONING': '辽宁队',
              'GUANGZHOU': '广州队', 'SICHUAN': '四川队', 'HUBEI': '湖北队', 'SHANXI1': '陕西队', 'SHENZHEN': '深圳队',
              'NEIMENG': '内蒙队', 'HEILONGJIANG': '黑龙江队', 'SHANXI2': '山西队'}


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
    return score


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

    if len(team_score) == 0:
        is_submit = False
        used_seconds = 0
    else:
        team_score = team_score[0]
        is_submit = team_score.submitted
        used_seconds = team_score.elapsed_seconds

    return {'id': team_user.id, 'name': NAME_TEAMS[account], 'pinyin': account, 'progress': 0,
            'is_submit': is_submit, 'used_seconds': used_seconds}


def get_team_user(account):
    team_user = User.objects.filter(account=account)
    if len(team_user) == 0:
        team_user = User.objects.create(account=account)
    else:
        team_user = team_user[0]
    return team_user
