# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 12:25
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trigger', '0004_auto_20151207_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triggerevent',
            name='description',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='triggerrule',
            name='configuration',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
