#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


from . import views
from django.conf.urls import url
from django.contrib import admin


# for mainline
urlpatterns = [
    url(r'^list/?',
        views.list,
        name='list'),
    url(r'^download/?',
        views.download,
        name='download'),
    url(r'^firmware/?',
        views.firmware_list,
        name='firmware_list'),
    url(r'^admin/', admin.site.urls),
]


# for debug
urlpatterns += [
    url(r'^task/areas/?',
        views.area_list,
        name='area_list'),
    url(r'^task/uuids/?',
        views.uuid_list,
        name='uuid_list'),
    url(r'^task/fdevs/?',
        views.fdev_list,
        name='fdev_list'),
]

from . import task



