# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgradeserver_lua', '0011_auto_20170919_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmware',
            name='name',
            field=models.FileField(unique=True, upload_to=b'', verbose_name='\u4e0a\u4f20\u6587\u4ef6'),
        ),
    ]