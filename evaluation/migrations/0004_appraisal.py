# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-01 20:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0003_auto_20170801_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluation.Evaluation')),
            ],
        ),
    ]