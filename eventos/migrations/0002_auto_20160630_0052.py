# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='complemento',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
