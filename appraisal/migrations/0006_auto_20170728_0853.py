# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-28 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0005_question_this'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='this',
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.CharField(default='', max_length=3000),
        ),
    ]