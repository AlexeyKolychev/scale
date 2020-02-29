# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-30 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def link_jobs_and_recipes(apps, schema_editor):
    # Go through all of the nodes and update their jobs/recipes to point to the node
    RecipeNode = apps.get_model('recipe', 'RecipeNode')

    total_count = RecipeNode.objects.all().count()
    if not total_count:
        return

    print('\nSetting recipe_node field for jobs/recipes')
    done_count = 0
    fail_count = 0
    for n in RecipeNode.objects.all():
        if n.job:
            n.job.recipe_node = n
        elif n.sub_recipe:
            n.sub_recipe.recipe_node = n
        done_count += 1
        percent = (float(done_count) / float(total_count)) * 100.00
        print('Progress: %i/%i (%.2f%%)' % (done_count, total_count, percent))

    print ('Migration finished. Failed: %i' % fail_count)

class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0038_add_recipe_recipe_node'),
        ('job', '0058_job_recipe_node')
    ]

    operations = [
        migrations.RunPython(link_jobs_and_recipes)
    ]
