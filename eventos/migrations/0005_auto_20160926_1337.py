# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-26 13:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_auto_20160829_1226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inscriuser',
            options={'ordering': ['user']},
        ),
    ]
