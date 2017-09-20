# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgradeserver_lua', '0007_auto_20170918_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firmware',
            name='succ',
        ),
        migrations.AddField(
            model_name='firmware',
            name='is_generated',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u751f\u6210'),
        ),
        migrations.AddField(
            model_name='firmware',
            name='is_important',
            field=models.BooleanField(default=False, verbose_name='\u91cd\u8981\u7248\u672c'),
        ),
    ]