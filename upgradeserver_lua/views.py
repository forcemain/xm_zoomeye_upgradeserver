#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import os
import json
from .wraps import upg_control
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .utils import analysis_download_body, find_version, dlog
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError


@csrf_exempt
def list(request):
    return HttpResponse(status=204)


# @upg_control
# @csrf_exempt
# def list(request, req_body=None, devid=None):
#     cur_version = req_body['CurVersion']
#     language = req_body['Language']
#     level = 1 if req_body['Expect'] == 'Important' else 0
#     # for version
#     if not settings.IDMAPS_DICT:
#         msg = 'versions not ready'
#         dlog.error(msg)
#         return HttpResponseServerError(msg)
#     version = find_version(settings.VERSIONS_DICT, devid, cur_version, level, language)
#     if version[0] is None:
#         dlog.error(version[1])
#         return HttpResponse(version[1], status=204)
#
#     return HttpResponse(json.dumps(version[0]))


@csrf_exempt
def download(request):
    # for param
    req_body_res = analysis_download_body(request.body)
    if req_body_res[0] is None:
        dlog.error(req_body_res[1])
        return HttpResponseBadRequest(req_body_res[1])
    req_body = req_body_res[0]
    f_path = os.path.join(
        '/download_file/', req_body['DevID'],
        req_body['Date'], req_body['FileName']
    )
    response = HttpResponse()
    response['X-Accel-Redirect'] = f_path
    return response


def firmware_list(request):
    if not settings.VERSIONS_DICT:
        return HttpResponseNotFound('versions not ready')
    return HttpResponse(json.dumps({'versions': settings.VERSIONS_DICT}))
