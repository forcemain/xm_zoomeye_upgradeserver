#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import os
import sys
import json


reload(sys)
sys.setdefaultencoding('utf8')


from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest


from .geoip import g_ip
from .models import UpgradeLog
from .utils import (analysis_list_body, analysis_download_body, find_version, get_client_ip,
                    area_can, uuid_can, date_can, dj_logging, get_extend_id)


def list(request):
    req_body_res = analysis_list_body(request.body)
    if req_body_res[0] is None:
        dj_logging(req_body_res[1])
        return HttpResponseBadRequest(req_body_res[1])
    req_body = req_body_res[0]
    extend_id = get_extend_id(req_body['DevID'], settings.IDMAPS_DICT)
    if extend_id[0] is None:
        dj_logging(extend_id[1])
        return HttpResponseBadRequest(extend_id[1])
    devid = extend_id[0]
    clientip = get_client_ip(request)
    if clientip is None:
        level = 1 if req_body['Expect'] == 'Important' else 0
        version = find_version(settings.VERSIONS_DICT, devid, req_body['CurVersion'], level, req_body['Language'])
        if version[0] is None:
            dj_logging(version[1])
            return HttpResponse(version[1], status=204)
        return HttpResponse(json.dumps(version[0], ensure_ascii=False))

    """ 日期控制-> UUID控制-> 区域控制
    
    1. datecontrol
    1.1. devid in cachemap ?
    1.1.1. no, continue uuidcontrol 
    1.1.2. yes, is expired ?
    1.1.2.1. yes, 204
    1.1.2.2. no, currentversion in dateRange ?
    1.1.2.2.1. yes, continue uuidcontrol
    1.1.2.2.2. no, 204
    
    
    2. uuidcontrol
    2.1. devid in cachemap ?
    2.1.1. no, continue areacontrol
    2.1.2. yes, uuid in cachemap ?
    2.1.2.1. no, 204
    2.1.2.2. yes, is expired ?
    2.1.2.2.1. yes, 204
    2.1.2.2.2. no, continue areacontrol
    
    3. areacontrol
    3.1. devid in cachemap ?
    3.1.1. no, 200
    3.1.2. yes, area in cachemap ?
    3.1.2.1. no, 204
    3.1.2.2. yes, is expired ?
    3.1.2.2.1. yes, 204
    3.1.2.2.2. no, 200
  
    """
    date_can_res, date_can_type = date_can(devid, req_body['CurVersion'])
    if not date_can_res:
        msg = '{0} datecontrol not allowed'.format(devid)
        dj_logging(msg)
        return HttpResponse(msg, status=204)
    uuid_can_res, uuid_can_type = uuid_can(req_body['UUID'], devid)
    if not uuid_can_res:
        msg = '{0} uuidcontrol not allowed'.format(req_body['UUID'])
        dj_logging(msg)
        return HttpResponse(msg, status=204)
    area = g_ip.city(clientip)
    if area is not None:
        area_can_res, area_can_type = area_can(area, devid)
        if not area_can_res:
            msg = '{0} areacontrol not allowed'.format(area)
            dj_logging(msg)
            return HttpResponse(msg, status=204)
    else:
        msg = '{0} not in geoip mmdb'.format(clientip)
        dj_logging(msg)

    level = 1 if req_body['Expect'] == 'Important' else 0
    version = find_version(settings.VERSIONS_DICT, devid, req_body['CurVersion'], level, req_body['Language'])
    if version[0] is None:
        dj_logging(version[1])
        return HttpResponse(version[1], status=204)
    return HttpResponse(json.dumps(version[0], ensure_ascii=False))


def download(request):
    req_body_res = analysis_download_body(request.body)
    if req_body_res[0] is None:
        dj_logging(req_body_res[1])
        return HttpResponseBadRequest(req_body_res[1])
    req_body = req_body_res[0]

    # 记录下载固件记录(但并不保证下载成功)
    extend_id = get_extend_id(req_body['DevID'], settings.IDMAPS_DICT)
    devid = extend_id[0]
    clientip = get_client_ip(request)
    area = g_ip.city(clientip)
    upgrade_log = UpgradeLog(uuid=req_body['UUID'], devid=devid, area=area or 'Unrecognized')
    upgrade_log.save()

    f_path = os.path.join(
        '/download_file/', devid,
        req_body['Date'], req_body['FileName']
    )
    response = HttpResponse()
    response['reserved_cdn_url'] = 'http://{0}:{1}{2}'.format(settings.SERVER_HOST, settings.SERVER_PORT, f_path)
    response['X-Accel-Redirect'] = f_path
    
    return response


def firmware_list(request):
    if not settings.VERSIONS_DICT:
        return HttpResponseNotFound('versions not ready')
    return HttpResponse(json.dumps({'versions': settings.VERSIONS_DICT}, ensure_ascii=False))


def area_list(request):
    if not settings.AREASCTL_DICT:
        return HttpResponseNotFound('areas not ready')
    return HttpResponse(json.dumps({'areas': settings.AREASCTL_DICT.keys()}, ensure_ascii=False))


def uuid_list(request):
    if not settings.UUIDSCTL_DICT:
        return HttpResponseNotFound('uuids not ready')
    return HttpResponse(json.dumps({'uuids': settings.UUIDSCTL_DICT.keys()}, ensure_ascii=False))


def date_list(request):
    if not settings.DATESCTL_DICT:
        return HttpResponseNotFound('dates not ready')
    return HttpResponse(json.dumps({'dates': settings.DATESCTL_DICT.keys()}, ensure_ascii=False))


def fdev_list(request):
    if not settings.FIRMWARES_DICT:
        return HttpResponseNotFound('firmwares not ready')
    return HttpResponse(json.dumps({'firmwares': settings.FIRMWARES_DICT.keys()}, ensure_ascii=False))
