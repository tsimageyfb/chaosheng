# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from questionnaire import http
import json, datetime, time


def index(request):
    context = {}
    return render(request, 'exam/index.html', context)
