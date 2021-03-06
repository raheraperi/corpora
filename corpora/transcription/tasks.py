from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from corpus.models import Recording, Sentence, Source
from transcription.models import \
    Transcription, TranscriptionSegment, AudioFileTranscription
from corpus.views.views import RecordingFileView
from django.contrib.sites.shortcuts import get_current_site

from corpora.utils.tmp_files import prepare_temporary_environment
from people.helpers import get_current_known_language_for_person

from transcription.utils import create_and_return_transcription_segments

from transcription.transcribe import transcribe_audio_sphinx
from django.utils import timezone
from django.core.files import File
import wave
import contextlib
import os
import stat
import commands
import ast
import sys
import requests
import urllib2
import json
import uuid
from subprocess import Popen, PIPE
import time


from django.core.cache import cache

import logging
logger = logging.getLogger('corpora')
logger_test = logging.getLogger('django.test')


@shared_task
def launch_transcription_api():
    num_jobs = cache.get('TRANSCRIPTION_JOBS', 0)

    # logger.debug('NUM_TRANSCRIPTION_JOBS: {0: <4f}'.format(num_jobs))

    '''
    Let's check jobs every minut, and maybe have a cooldown of 5 minutes
    so the initial get re4quests cause us to ensure that we're running a server,
    but after 5 minutes if there are no actual transcription jobs then we should
    just take the servers down
    '''

    # logger.debug('LAUNCHING')
    return "DISABLED CHANGING OF AUTOSCALINGGROUP"

    import boto3
    import os
    os.environ['PROJECT_NAME']
    client = boto3.client(
        'autoscaling',
        aws_access_key_id=os.environ['AWS_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET'],
        region_name='ap-southeast-2')

    response = client.set_desired_capacity(
            AutoScalingGroupName='asg-corpora-production-deepspeech',
            DesiredCapacity=1,
            HonorCooldown=False,
        )


@shared_task
def launch_watcher():
    # Use beat to schedule this
    last_queue = cache.get('JOBS_PING', [])
    num_jobs = cache.get('TRANSCRIPTION_JOBS', 0)
    last_queue.insert(0, num_jobs)

    count = 0
    for i in range(len(last_queue)-1):
        if last_queue[i] - last_queue[i+1] == 0:
            count = count + 1

    if count == 3:
        num_jobs = 0

    last_queue = cache.set('JOBS_PING', last_queue)
    # logger.debug('NUM_TRANSCRIPTION_JOBS: {0: <4f}'.format(num_jobs))

    if num_jobs <= 0:
        logger.debug('STOPPING')

        return "DISABLED CHANGING OF AUTOSCALINGGROUP"

        client = boto3.client(
            'autoscaling',
            aws_access_key_id=os.environ['AWS_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET'],
            region_name='ap-southeast-2')

        response = client.set_desired_capacity(
                AutoScalingGroupName='asg-corpora-production-deepspeech',
                DesiredCapacity=0,
                HonorCooldown=True,
            )


@shared_task
def transcribe_recordings_without_reviews():
    MAX_LOOP = 3500
    recordings = Recording.objects\
        .filter(transcription__isnull=True)\
        .distinct().order_by('created')

    # Once we're done with all the recordings,
    # let's see if there are some unfinished ones.
    if recordings.count() == 0:
        recordings = Recording.objects\
            .filter(quality_control__isnull=True)\
            .filter(transcription__text=None)\
            .distinct().order_by('created')

    total = recordings.count()

    start = timezone.now()

    if total == 0:
        return "No recordings to transcribe."

    logger.debug('Recordings that need reviewing: {0}'.format(total))

    recordings = recordings[:MAX_LOOP]

    source, created = Source.objects.get_or_create(
        source_name='Transcription API',
        source_type='M',
        source_url=settings.DEEPSPEECH_URL,
        author='Keoni Mahelona'
    )
    source.save()

    error = 0
    e = 'None'
    for recording in recordings:
        t, created = Transcription.objects.get_or_create(
                recording=recording,
                source=source,
            )

    count = 0.0
    for recording in recordings:
        transcribe_recording.apply_async(
            args=[recording.pk],
        )
        count = count+1

    if total > MAX_LOOP:
        t = MAX_LOOP
        left = total - MAX_LOOP
    else:
        t = total
        left = 0

    time = timezone.now()-start
    return "Done with {0} recordings. {1} to transcribe. Took {2}s" \
        .format(recordings.count(), left, time.total_seconds())


@shared_task
def transcribe_recording(pk):
    recording = Recording.objects.get(pk=pk)
    try:
        transcription = Transcription.objects.get(recording=recording)
    except MultipleObjectsReturned:
        transcriptions = Transcription.objects\
            .filter(recording=recording).order_by('pk')
        transcription = transcriptions.last()
        t = transcriptions.first()
        t.delete()

    start = timezone.now()
    if not transcription.text:
        try:
            # This should tell us if the file exists
            recording.audio_file_wav.open('rb')
            result = transcribe_audio_sphinx(
                recording.audio_file_wav.read(),
                timeout=60)
            recording.audio_file_wav.close()

            transcription.text = result['transcription'].strip()
            transcription.transcriber_log = result
            transcription.save()
            dt = timezone.now() - start
            return "Transcribed {0} in {1}s".format(
                transcription.text, dt.total_seconds())

        except Exception as e:
            logger.error(e)
            transcription.delete()
            return str(e)
    else:
        return "Already transcribed: {0}".format(transcription.text)


@shared_task
def delete_transcriptions_for_approved_recordings():
    transcriptions = Transcription.objects\
        .filter(recording__quality_control__approved=True)
    transcriptions.delete()
