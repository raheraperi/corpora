# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0017_auto_20171113_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knownlanguage',
            name='level_of_proficiency',
            field=models.IntegerField(blank=True, choices=[(1, 'Native Speaker - Beginner'), (2, 'Native Speaker - Intermediate'), (3, 'Native Speaker - Advanced'), (4, 'Near Native Speaker - Beginner'), (5, 'Near Native Speaker - Intermediate'), (6, 'Near Native Speaker - Advanced'), (7, 'Second Language Learner - Beginner'), (8, 'Second Language Learner - Intermediate'), (9, 'Second Language Learner - Advanced')], null=True),
        ),
    ]