#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import re
import os
import sys
import json
import chardet
from copy import deepcopy
from django.conf import settings
from django.utils import timezone


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
        devid = ''.join([uuid[:8], 'X'*5, '0'*4,
                         uuid[17:]])

    return uuid, devid


def analysis_list_body(data):
    try:
        req_body = json.loads(data)
    except ValueError:
        return None, 'request body {0} is not a json'.format(data)

    if 'UUID' not in req_body or \
       'DevID' not in req_body or \
       'DevType' not in req_body or \
       'CurVersion' not in req_body or \
       'Expect' not in req_body or \
       'Language' not in req_body or \
       'Manual' not in req_body:

        return None, '{0} is a invalid message'.format(data)

    return req_body,


def analysis_download_body(data):
    try:
        req_body = json.loads(data)
    except ValueError:
        return None, 'request body {0} is not a json'.format(data)

    if 'UUID' not in req_body or \
       'DevID' not in req_body or \
       'FileName' not in req_body or \
       'Date' not in req_body or \
       'Manual' not in req_body:

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
    version_info = {}

    devid_key = '_'.join(('DevID', devid))
    version = versions.get(devid_key, None)
    if version is None:
        return None, '{0} not in versions'.format(devid_key)

    rds_key = 'upg::datecontrol::{0}'.format(devid)
    rds_val = settings.REDIS_CONN.hmget(rds_key)
    if rds_val['upg_once']:
        if version[level]:
            version_info = deepcopy(version[level])
    else:
        if version[level] and version[level]['Date'] > cur_version:
            version_info = deepcopy(version[level])

    if not version_info:
        return None, '{0} already latest {1} version'.format(devid, level and 'Important' or '')

    if 'Chinese' in language:
        l_lang = ['SimpChinese', 'Chinese']
    else:
        l_lang = ['English']

    f_name = None
    d_path = os.path.join(settings.UPGRADE_PATH, version_info['DevID'], version_info['Date'])
    for lang in l_lang:
        l_name = ''.join(('ChangeLog_', lang, '.dat'))
        f_name = os.path.join(d_path, l_name)
        if os.path.exists(f_name):
            break
    try:
        with open(f_name) as fd:
            version_info['ChangeLog'] = s_encode(s_decode(fd.read()))
    except (TypeError, IOError):
            version_info['ChangeLog'] = u'xm_zoomeye_upgradeserver automic upgrade'

    return version_info,


def get_client_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.META:
        ip = request.META['REMOTE_ADDR']
    else:
        ip = None

    return ip


def area_can(area, devid):
    if not settings.AREASCTL_DICT:
        return True, 0
    if devid not in settings.DEVIDCTL_DICT:
        return True, 0
    areas = []
    area_list = area.split('_') if '_' in area else [area]
    for k, v in enumerate(area_list, start=1):
        area_key = '_'.join(area_list[:k]) if k > 1 else v
        areas.append(area_key)

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


def date_can(uuid, devid, curversion):
    rds_key = 'upg::datecontrol::{0}'.format(devid)
    rds_val = settings.REDIS_CONN.hmget(rds_key)
    if not rds_val:
        return True, 0
    time = timezone.now()
    if (rds_val['start_time'] and time < rds_val['start_time']) or \
       (rds_val['end_time'] and time > rds_val['end_time']):
        return False, 1
    if (rds_val['start_date'] and curversion < rds_val['start_date'].strftime('%Y-%m-%d')) or \
       (rds_val['end_date'] and curversion > rds_val['end_date'].strftime('%Y-%m-%d')):
        return False, 1
    if rds_val['upg_once']:
        rds_key = 'upg::datecontrol::{0}::{1}::upgraded'.format(devid, uuid)
        if settings.REDIS_CONN.exists(rds_key):
            return False, 1
    return True, 1


def dj_logging(msg):
    log = '=> upgradeserver_lua: {0}{1}'.format(msg, os.linesep)
    sys.stderr.write(log)

