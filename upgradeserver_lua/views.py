#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import os
import json
from .wraps import upg_control
from .models import IdMapCache, VersionCache
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .utils import analysis_download_body, get_extend_id, find_version, dlog
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError


@upg_control
@csrf_exempt
def list(request, req_body=None, devid=None):
    cur_version = req_body['CurVersion']
    language = req_body['Language']
    level = 1 if req_body['Expect'] == 'Important' else 0
    # for version
    try:
        versions_ins = VersionCache.objects.get(pk=1)
    except VersionCache.DoesNotExist:
        dlog.error('versions not ready')
        return HttpResponseServerError('versions not ready')
    versions = json.loads(versions_ins.data)
    version = find_version(versions, devid, cur_version, level, language)
    if version[0] is None:
        dlog.error(version[1])
        return HttpResponse(version[1], status=204)

    return HttpResponse(json.dumps(version[0]))


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
    data = {}
    versions_ins = get_object_or_404(VersionCache, pk=1)
    versions = json.loads(versions_ins.data)

    data.update({'versions': versions})

    return HttpResponse(json.dumps(data))


def firmware_dates(request, devid):
    data = {}
    versions_ins = get_object_or_404(VersionCache, pk=1)
    versions = json.loads(versions_ins.data)

    key = '_'.join(('DevID', devid))
    data.update({'versions': {devid: versions[key]} if key in versions else {}})

    return HttpResponse(json.dumps(data))


def firmware_detail(request, devid, date):
    return HttpResponse('ok')
