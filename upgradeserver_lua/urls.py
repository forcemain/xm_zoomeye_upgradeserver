#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from . import views


urlpatterns = [
    url(r'^list/?',
        views.list,
        name='list'),
    url(r'^download/?',
        views.download,
        name='download'),
    url(r'^firmware/$',
        views.firmware_list,
        name='firmware_list'),
    url(r'^firmware/([0-9a-zA-Z]{24})/?',
        views.firmware_dates,
        name='firmware_dates'),
    url(r'^firmware/([0-9a-zA-Z]{24})/([0-9]{4}-[0-9]{2}-[0-9]{2})/?',
        views.firmware_detail,
        name='firmware_detail'),
    url(r'^admin/', admin.site.urls),
]

from . import task


