#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class UpgServerConfig(AppConfig):
    name = 'upgradeserver_lua'


class UpgSuitConfig(DjangoSuitConfig):
    layout = 'vertical'
