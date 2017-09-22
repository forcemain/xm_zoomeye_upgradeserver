#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import re
import os
import json
import chardet
from logging import getLogger
from django.conf import settings
from django.utils import timezone


dlog = getLogger(settings.DLOGGER)


def s_decode(strs, dec='utf-8'):
    encoding = chardet.detect(strs).get('encoding', dec)
    return strs.decode(encoding or dec, 'replace')


def s_encode(strs, enc='utf-8'):
    try:
        return s_decode(strs).encode(enc)
    except TypeError as e:
        return strs.encode(enc)


def uuid2devid(uuid):
    id_pattern = re.compile(r'^[0-9A-Za-z]{16,24}$')
    match = re.match(id_pattern, uuid)
    if not match:
        return None, '{0} invalid device uuid'.format(uuid)
    if uuid[5] < '5':
        devid = ''.join([uuid[:8], 'X'*11,
                         uuid[19:]])
    else:
        devid = ''.join([uuid[:8],
                         uuid[8:13].replace('2', '0').replace('3', '1'), '0'*4,
                         uuid[17:]])

    return uuid, devid


def analysis_list_body(data):
    try:
        req_body = json.loads(data)
    except ValueError as e:
        return None, 'request body {0} is not a json'.format(data)

    if 'UUID' not in req_body or \
        not isinstance(req_body['UUID'], (str, unicode)) or \
            len(req_body['UUID']) == 0 or \
            len(req_body['UUID']) > 64 or \
            'DevID' not in req_body or \
            not isinstance(req_body['DevID'], (str, unicode)) or \
            len(req_body['DevID']) == 0 or \
            len(req_body['DevID']) > 64 or \
            'DevType' not in req_body or \
            not isinstance(req_body['DevType'], (str, unicode)) or \
            len(req_body['DevType']) == 0 or \
            'CurVersion' not in req_body or \
            not isinstance(req_body['CurVersion'], (str, unicode)) or \
            len(req_body['CurVersion']) != 10 or \
            'Expect' not in req_body or \
            not isinstance(req_body['Expect'], (str, unicode)) or \
            len(req_body['Expect']) == 0 or \
            'Language' not in req_body or \
            not isinstance(req_body['Language'], (str, unicode)) or \
            len(req_body['Language']) == 0 or \
            'Manual' not in req_body or \
            not isinstance(req_body['Manual'], (str, unicode)) or \
            len(req_body['Manual']) == 0:

        return None, '{0} is a invalid message'.format(data)

    return req_body,


def analysis_download_body(data):
    try:
        req_body = json.loads(data)
    except ValueError as e:
        return None, 'request body {0} is not a json'.format(data)

    if 'UUID' not in req_body or \
            not isinstance(req_body['UUID'], (str, unicode)) or \
            len(req_body['UUID']) == 0 or \
            len(req_body['UUID']) > 64 or \
            'DevID' not in req_body or \
            not isinstance(req_body['DevID'], (str, unicode)) or \
            len(req_body['DevID']) == 0 or \
            len(req_body['DevID']) > 64 or \
            'FileName' not in req_body or \
            not isinstance(req_body['FileName'], (str, unicode)) or \
            len(req_body['FileName']) == 0 or \
            'Date' not in req_body or \
            not isinstance(req_body['Date'], (str, unicode)) or \
            len(req_body['Date']) != 10 or \
            'Manual' not in req_body or \
            not isinstance(req_body['Manual'], (str, unicode)) or \
            len(req_body['Manual']) == 0:

        return None, '{0} is a invalid message'.format(data)

    return req_body,


def get_extend_id(srcid, idmap):
    idinfo = uuid2devid(srcid)
    if idinfo[0] is None:
        return idinfo
    uuid, devid = idinfo
    idmap_key = '_'.join(('SrcID', devid))
    idmap_val = idmap.get(idmap_key, None)

    dstid = devid if idmap_val is None else idmap_val
    if len(dstid) != 24:
        return None, '{0} length is {1}, invalid devid'.format(dstid, len(dstid))
    return dstid,


def find_version(versions, devid, cur_version, level, language):
    latest = {}

    devid_key = '_'.join(('DevID', devid))
    version = versions.get(devid_key, None)
    if version is None:
        return None, '{0} not in versions'.format(devid_key)

    if version[0] and 'Date' in version[0] and version[0]['Date'] > cur_version:
        latest = version[0]
        latest['FileLevel'] = level

    if 'Date' not in latest:
        return None, '{0} version {1} level {2} not found'.format(devid_key, cur_version, level)

    l_name = ''.join(('ChangeLog', language, '.dat'))
    d_path = os.path.join(settings.UPGRADE_PATH, latest['DevID'], latest['Date'])
    try:
        with open(os.path.join(d_path, l_name)) as fd:
            latest['ChangeLog'] = s_encode(s_decode(fd.read()))
    except IOError as e:
        if language != 'Chinese':
            try:
                with open(os.path.join(d_path, 'ChangeLog_Chinese.dat')) as fd:
                    latest['ChangeLog'] = s_encode(s_decode(fd.read()))
            except IOError as e:
                latest['ChangeLog'] = ''
        else:
            latest['ChangeLog'] = ''

    return latest,


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

    if not settings.AREASCTL_DICT:
        return True, 0

    area_val = None
    for area_key in areas:
        area_val = settings.AREASCTL_DICT.get(area_key, None)
        if area_val is not None:
            break
    if area_val is None:
        return False, 0
    time = timezone.now()
    if (area_val['start_time'] and time < area_val['start_time']) or \
       (area_val['end_time'] and time > area_val['end_time']):
        return False, 1
    return True, 1


def uuid_can(uuid, devid):
    if not settings.UUIDSCTL_DICT:
        return True, 0
    if devid not in settings.UUIDSCTL_DICT:
        return True, 0
    if uuid in settings.UUIDSCTL_DICT[devid]:
        uuid_val = settings.UUIDSCTL_DICT[devid][uuid]
        time = timezone.now()
        if (uuid_val['start_time'] and time < uuid_val['start_time']) or \
           (uuid_val['end_time'] and time > uuid_val['end_time']):
            return False, 1
        return True, 1
    else:
        return False, 1