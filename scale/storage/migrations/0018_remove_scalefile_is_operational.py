# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-01 14:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0017_remove_scalefile_data_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scalefile',
            name='is_operational',
        ),
    ]
