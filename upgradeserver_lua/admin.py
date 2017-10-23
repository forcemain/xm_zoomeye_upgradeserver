#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


from django.contrib import admin
from .models import AreaControl, UuidControl, DateControl, Firmware


class UuidControlAdmin(admin.ModelAdmin):
    ordering = ['uuid']
    list_per_page = 20
    search_fields = ['uuid', 'notes']
    fields = ['uuid', 'devid', 'start_time', 'end_time', 'notes']
    list_display = ['id', 'uuid', 'devid', 'is_expired', 'start_time', 'end_time', 'notes']


class AreaControlAdmin(admin.ModelAdmin):
    ordering = ['area']
    list_per_page = 20
    search_fields = ['area', 'notes']
    fields = ['area', 'start_time', 'end_time', 'notes']
    list_display = ['id', 'area', 'is_expired', 'start_time', 'end_time', 'notes']


class DateControlAdmin(admin.ModelAdmin):
    ordering = ['devid']
    list_per_page = 20
    search_fields = ['devid', 'notes']
    fields = ['devid', 'start_time', 'end_time', 'start_date', 'end_date', 'notes']
    list_display = ['id', 'devid', 'is_expired', 'start_time', 'end_time', 'start_date', 'end_date', 'notes']


class FirmwareAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_per_page = 20
    fields = ['name', 'is_important', 'date', 'notes']
    search_fields = ['name', 'notes']
    list_display = ['id', 'name', 'is_important', 'is_generated', 'date', 'notes']


admin.site.register(UuidControl, UuidControlAdmin)
admin.site.register(DateControl, DateControlAdmin)
admin.site.register(AreaControl, AreaControlAdmin)
admin.site.register(Firmware, FirmwareAdmin)
