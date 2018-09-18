# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-27 03:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0034_qualitycontrol_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualitycontrol',
            name='machine',
            field=models.BooleanField(default=False, help_text='Boolean to indicate if a machine made the review.'),
        ),
        migrations.AddField(
            model_name='qualitycontrol',
            name='source',
            field=models.ForeignKey(blank=True, help_text='Used to identify machines.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.Source'),
        ),
    ]
