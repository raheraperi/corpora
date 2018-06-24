# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-02 04:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0002_auto_20180515_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcription',
            name='source',
            field=models.ForeignKey(blank=True, help_text='The source should be the transcription API.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.Source'),
        ),
    ]