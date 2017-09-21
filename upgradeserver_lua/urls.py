#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


from . import views
from django.conf.urls import url
from django.contrib import admin


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
    url(r'^admin/', admin.site.urls),
]

from . import task



