# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httplib
import json
from questionnaire import settings
from django.http import HttpResponse


def wrap_ok_response(result):
    return HttpResponse(json.dumps({'code': 0, 'message': '', 'data': result}), content_type='application/json')


def wrap_bad_response(code, msg):
    return HttpResponse(json.dumps({'code': code, 'message': msg}), content_type='application/json')


def do_get(url):
    data = {}
    conn = httplib.HTTPConnection(settings.HTTP_HOST)
    try:
        conn.request("GET", url)
        res = conn.getresponse()
        if res.status == 200:
            raw = json.loads(res.read())
            if raw["code"] == 0:
                data = raw["data"]
            else:
                data = raw["message"]
        else:
            data = "error"
        return data
    except:
        print "error of get: "+url
        return data
    finally:
        conn.close()


def do_post(url, params):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(settings.HTTP_HOST)
    try:
        conn.request("POST", url, json.dumps(params), headers)
        res = conn.getresponse()
        if res.status == 200:
            raw = json.loads(res.read())
            if raw["code"] == 0:
                data = raw["data"]
                return data
            return raw["dev_message"]
        return "error of post response: " + url
    except:
        print "error of post: " + url
    finally:
        conn.close()
