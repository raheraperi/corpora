# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-10 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0038_recording_audio_file_wav_md5'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='qualitycontrol',
            index=models.Index(fields=['object_id', 'content_type'], name='corpus_qual_object__11b3d6_idx'),
        ),
    ]
