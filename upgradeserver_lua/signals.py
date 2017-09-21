#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


from django.conf import settings
from .models import Firmware, AreaControl, UuidControl
from django.db.models.signals import post_save, post_delete


def update_area_cache():
    settings.AREASCTL_DICT.clear()
    for item in AreaControl.objects.values():
        settings.AREASCTL_DICT.update({
            item['area']: {'start_time': item['start_time'], 'end_time': item['end_time'], 'notes': item['notes']}
        })


def update_uuid_cache():
    settings.UUIDSCTL_DICT.clear()
    for item in UuidControl.objects.values():
        settings.UUIDSCTL_DICT.setdefault(item['devid'], {})
        settings.UUIDSCTL_DICT.update({
            item['devid']: {'start_time': item['start_time'], 'end_time': item['end_time'], 'notes': item['notes']}
        })


def update_firmware_cache():
    settings.FIRMWARES_DICT.clear()
    for item in Firmware.objects.values():
        settings.FIRMWARES_DICT.update({
            item['name']: {'date': item['date'], 'is_generated': item['is_generated'],
                           'is_important': item['is_important'], 'notes': item['notes']}
        })


def update_memory_cache(sender, **kwargs):
    update_area_cache()
    update_uuid_cache()
    update_firmware_cache()


post_save.connect(update_memory_cache)
post_delete.connect(update_memory_cache)

