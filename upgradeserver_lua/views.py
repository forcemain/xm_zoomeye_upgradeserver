#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import os
import json
from .geoip import g_ip
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from .utils import (analysis_list_body, analysis_download_body, find_version, get_client_ip, area_can, uuid_can, dlog,
                    get_extend_id)


def list(request):
    req_body_res = analysis_list_body(request.body)
    if req_body_res[0] is None:
        dlog.error(req_body_res[1])
        return HttpResponseBadRequest(req_body_res[1])
    req_body = req_body_res[0]
    extend_id = get_extend_id(req_body['DevID'], settings.IDMAPS_DICT)
    if extend_id[0] is None:
        dlog.error(extend_id[1])
        return HttpResponseBadRequest(extend_id[1])
    devid = extend_id[0]
    clientip = get_client_ip(request)
    if clientip is None:
        level = 1 if req_body['Expect'] == 'Important' else 0
        # for version
        version = find_version(settings.VERSIONS_DICT, devid, req_body['CurVersion'], level, req_body['Language'])
        if version[0] is None:
            dlog.error(version[1])
            return HttpResponse(version[1], status=204)
        return HttpResponse(json.dumps(version[0]))
    uuid_can_res, uuid_can_type = uuid_can(req_body['UUID'], devid)
    if not uuid_can_res:
        msg = '{0} not allowed'.format(req_body['UUID'])
        dlog.warn(msg)
        return HttpResponse(msg, status=204)
    if uuid_can_type == 0:
        area = g_ip.city(clientip)
        if area is not None:
            area_can_res, area_can_type = area_can(area)
            if not area_can_res:
                msg = '{0} not allowed'.format(clientip)
                dlog.warn(msg)
                return HttpResponse(msg, status=204)
        else:
            msg = '{0} not in geoip mmdb'.format(clientip)
            dlog.warn(msg)
    level = 1 if req_body['Expect'] == 'Important' else 0
    # for version
    version = find_version(settings.VERSIONS_DICT, devid, req_body['CurVersion'], level, req_body['Language'])
    if version[0] is None:
        dlog.error(version[1])
        return HttpResponse(version[1], status=204)
    return HttpResponse(json.dumps(version[0]))


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
