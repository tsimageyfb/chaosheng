# -*- coding: utf-8 -*-
from .models import Exam, Question


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
