# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 16:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0008_auto_20170609_1443'),
        ('job', '0027_auto_20170615_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobInputFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_input', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('input_file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='storage.ScaleFile')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='job.Job')),
            ],
            options={
                'db_table': 'job_input_file',
            },
        ),
    ]
