# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import httplib
import json
from questionnaire import settings
from django.http import JsonResponse


def wrap_ok_response(result):
    response = JsonResponse({'code': 0, 'message': '', 'data': result}, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def wrap_bad_response(code, msg):
    response = JsonResponse({'code': code, 'message': msg}, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


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
