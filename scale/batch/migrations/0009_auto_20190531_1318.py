# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-05-31 13:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0008_auto_20190226_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batchjob',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='batchjob',
            name='job',
        ),
        migrations.RemoveField(
            model_name='batchjob',
            name='superseded_job',
        ),
        migrations.RemoveField(
            model_name='batchrecipe',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='batchrecipe',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='batchrecipe',
            name='superseded_recipe',
        ),
        migrations.DeleteModel(
            name='BatchJob',
        ),
        migrations.DeleteModel(
            name='BatchRecipe',
        ),
    ]
