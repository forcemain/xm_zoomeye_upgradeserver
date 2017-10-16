#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


import os
import re
import json
import stat
import zipfile
import shutil
from .models import Firmware
from django.conf import settings
from .utils import get_extend_id, dj_logging
from apscheduler.schedulers.background import BackgroundScheduler
from .signals import update_area_cache, update_uuid_cache, update_firmware_cache


FIRMWARE_PATTERN = re.compile(r'''(?<=\.)(?P<date>[0-9]+)(?=\.bin|_ALL\.bin|_all\.bin)''')


def get_version_info(date, devid_root):
    version_info = {}

    devid_date_root = os.path.join(devid_root, date)
    if not os.path.exists(devid_date_root):
        return None, '{0} not exists'.format(devid_date_root)

    level_pattern = re.compile(r'^Level_([01]).dat$')
    firmware_pattern = re.compile(r'^.*.bin$')
    for f in os.listdir(devid_date_root):
        f_path = os.path.join(devid_date_root, f)
        level_match = re.match(level_pattern, f)

        if level_match:
            # version_info['FileLevel'] = int(level_match.group(1))
            version_info['FileLevel'] = 0

        firmware_match = re.match(firmware_pattern, f)
        if firmware_match:
            version_info['FileName'] = f
            version_info['FileSize'] = os.path.getsize(f_path)

    if 'FileLevel' not in version_info or \
       'FileName' not in version_info or \
       'FileSize' not in version_info:
        return None, '{0} no FileLevel or FileName or FileSize'.format(devid_date_root)

    return version_info['FileName'], version_info['FileSize'], version_info['FileLevel']


def find_version(devid, root):
    latest = {}
    important = {}

    devid_root = os.path.join(root, devid)
    if not os.path.exists(devid_root):
        return None, '{0} not exists'.format(devid_root)

    date_pattern = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    for d in os.listdir(devid_root):
        match = re.match(date_pattern, d)
        if not match:
            continue

        version_info = get_version_info(d, devid_root)
        if version_info[0] is None:
            return version_info
        fname, fsize, flevel = version_info
        if 'Date' not in latest or d > latest['Date']:
            latest['DevID'] = devid
            latest['Date'] = d
            latest['FileName'] = fname
            latest['FileSize'] = fsize
            latest['FileLevel'] = flevel

    if 'Date' not in latest and 'Date' not in important:
        return None, '{0} not date found'.format(devid_root)

    return latest, important


def get_firmware_devid(path):
    srcid = None
    try:
        unzip_obj = zipfile.ZipFile(path, 'r')
    except (IOError, RuntimeError) as e:
        return srcid, e
    for f in unzip_obj.namelist():
        if f == 'InstallDesc':
            f_data = unzip_obj.read(f)
            if 'DevID' in f_data:
                try:
                    srcid = json.loads(f_data)['DevID']
                except (KeyError, ValueError) as e:
                    return srcid, 'InstallDesc {0}'.format(e)
                break
    if srcid is None:
        return srcid, 'no devid in InstallDesc'
    if not settings.IDMAPS_DICT:
        return None, 'idmap not ready'
    extend_id = get_extend_id(srcid, settings.IDMAPS_DICT)
    if extend_id[0] is None:
        return extend_id
    devid = extend_id[0]
    return devid,


def get_firmware_date(path):
    match = re.search(FIRMWARE_PATTERN, path)
    if not match:
        return None, 'invalid pattern name.'
    match_date = match.groupdict()['date']
    fdate = '-'.join((match_date[:4], match_date[4:6], match_date[6:]))

    return fdate,


def auto_generate_dirs():
    os.chdir(settings.MEDIA_ROOT)
    for f in os.listdir('.'):
        f_mode = os.lstat(f).st_mode
        if not (stat.S_ISREG(f_mode) and f.endswith('.bin')):
            continue

        firmware = Firmware.objects.filter(name=f)
        fdate_res = get_firmware_date(f)
        if fdate_res[0] is None:
            dj_logging('{0}, {1}'.format(f, fdate_res[1]))
            firmware and firmware.update(is_generated=False, notes=fdate_res[1])
            continue
        fdate = fdate_res[0]
        devid_res = get_firmware_devid(f)
        if devid_res[0] is None:
            dj_logging('{0}, {1}'.format(f, devid_res[1]))
            firmware and firmware.update(is_generated=False, notes=devid_res[1])
            continue
        devid = devid_res[0]

        date_dir = os.path.join(devid, fdate)
        if os.path.exists(date_dir):
            shutil.rmtree(date_dir)
        os.makedirs(date_dir)

        shutil.move(f, date_dir)
        flevel = 1 if (firmware and firmware[0].is_important) else 0
        create_files = [
            'Level_{0}.dat'.format(flevel),
            'ChangeLog_Chinese.dat',
            'ChangeLog_English.dat'
        ]
        for cf in create_files:
            cf_path = os.path.join(date_dir, cf)
            print 'cf path', cf_path
            with open(cf_path, 'w+b') as fd:
                fd.write('automic created')

        firmware.update(is_generated=True)


def update_version_cache():
    data = {}
    root = settings.UPGRADE_PATH
    devid_pattern = re.compile(r'^[0-9A-Za-z]{24}$')
    for d in os.listdir(root):
        match = re.match(devid_pattern, d)
        if not match:
            continue
        version = find_version(d, root)
        if version[0] is None:
            continue
        key = '_'.join(('DevID', d))
        data[key] = version

    settings.VERSIONS_DICT.update(data)


def update_database_cache():
    update_area_cache()
    update_uuid_cache()
    update_firmware_cache()


scheduler = BackgroundScheduler()

scheduler.add_job(update_database_cache)
scheduler.add_job(update_version_cache)
scheduler.add_job(auto_generate_dirs)
scheduler.add_job(update_version_cache, 'interval', seconds=5)
scheduler.add_job(auto_generate_dirs, 'interval', seconds=5)

scheduler.start()
