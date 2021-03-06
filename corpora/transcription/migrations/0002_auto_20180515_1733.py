# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-15 05:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transcription',
            options={},
        ),
        migrations.AlterField(
            model_name='transcription',
            name='corrected_text',
            field=models.CharField(blank=True, help_text='The corrected text', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='transcription',
            name='text',
            field=models.CharField(help_text='The initial transcribed text', max_length=1024),
        ),
    ]
