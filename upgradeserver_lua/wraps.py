#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import json
from .geoip import g_ip
from django.conf import settings
from django.utils import timezone
from .models import AreaControl, UuidControl
from .utils import analysis_list_body, get_extend_id, dlog
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError


def get_client_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.META:
        ip = request.META['REMOTE_ADDR']
    else:
        ip = None

    return ip


def area_can(area):
    areas = []
    area_list = area.split('_') if '_' in area else [area]
    for k, v in enumerate(area_list, start=1):
        area_key = ':'.join(area_list[:k]) if k > 1 else v
        areas.append(area_key)

    area_objs = AreaControl.objects
    if area_objs.count() == 0:
        return True, 0
    area_arrs = area_objs.filter(area__in=areas)
    if not area_arrs:
        return False, 0
    area = area_arrs[0]
    time = timezone.now()
    if (area.start_time and time < area.start_time) or (area.end_time and time > area.end_time):
        return False, 1
    return True, 1


def uuid_can(uuid, devid):
    uuid_objs = UuidControl.objects
    if uuid_objs.count() == 0:
        return True, 0
    devid_list = uuid_objs.filter(devid=devid)
    if not devid_list:
        return True, 0
    uuid_list = devid_list.filter(uuid=uuid)
    if uuid_list:
        uuid = uuid_list[0]
        time = timezone.now()
        if (uuid.start_time and time < uuid.start_time) or (uuid.end_time and time > uuid.end_time):
            return False, 1
        return True, 1
    else:
        return False, 1


def upg_control(func):
    def _decorator(request):
        # 解析request body
        req_body_res = analysis_list_body(request.body)
        if req_body_res[0] is None:
            dlog.error(req_body_res[1])
            return HttpResponseBadRequest(req_body_res[1])
        req_body = req_body_res[0]
        # 获取最终的devid
        if not settings.IDMAPS_DICT:
            msg = 'idmap not ready'
            dlog.error(msg)
            return HttpResponseServerError(msg)
        extend_id = get_extend_id(req_body['DevID'], settings.IDMAPS_DICT)
        if extend_id[0] is None:
            dlog.error(extend_id[1])
            return HttpResponseBadRequest(extend_id[1])
        devid = extend_id[0]
        clientip = get_client_ip(request)
        if clientip is None:
            return func(request, req_body, devid)
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
        return func(request, req_body, devid)
    return _decorator
