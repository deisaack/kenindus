# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-24 10:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisal',
            name='question',
        ),
    ]