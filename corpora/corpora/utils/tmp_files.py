
from django.conf import settings
import os
import commands
import stat

from boto.s3.connection import S3Connection

import logging
logger = logging.getLogger('corpora')


def get_file_url(f, expires=60):
    s3 = S3Connection(settings.AWS_ACCESS_KEY_ID_S3,
                      settings.AWS_SECRET_ACCESS_KEY_S3,
                      is_secure=True)
    # Create a URL valid for 60 seconds.
    return s3.generate_url(expires, 'GET',
                           bucket=settings.AWS_STORAGE_BUCKET_NAME,
                           key=f.name)


def prepare_temporary_environment(model, test=False):
    # This method gets strings for necessary media urls/directories and create
    # tmp folders/files
    # NOTE: we use "media" that should be changed.

    file = model.audio_file
    absolute_directory = ''

    if 'http' in file.url:
        file_path = file.url
    else:
        file_path = settings.MEDIA_ROOT + file.name

    tmp_stor_dir = os.path.join(
        '/tmp',
        "{0}_files".format(settings.PROJECT_NAME),
        str(model.__class__.__name__)+str(model.pk))

    paths = [
        '/tmp/{0}_files'.format(settings.PROJECT_NAME),
        tmp_stor_dir]

    for path in paths:
        try:
            os.makedirs(path)
        except OSError as e:
            es = "{0}".format(str(e))
            if 'file exists' in es.lower():
                continue
            else:
                raise e
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                 stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
                 stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)

    tmp_file = os.path.join(
        tmp_stor_dir,
        file.name.split('/')[-1].replace(' ', ''))

    if os.path.exists(tmp_file):
        # Ensure permissions are correct.
        os.chmod(tmp_file, stat.S_IRUSR | stat.S_IWUSR |
                 stat.S_IRGRP | stat.S_IROTH)
        return file_path, tmp_stor_dir, tmp_file, absolute_directory

    # Will just replace file since we only doing one encode.
    if 'http' in file_path:
        url = get_file_url(file)
        code = 'wget "'+url+'" -O ' + tmp_file
    else:
        code = "cp '%s' '%s'" % (file_path, tmp_file)
    result = commands.getstatusoutput(code)

    try:
        logger.debug(result[1])
        result = ' '.join([str(i) for i in result])
    except:
        logger.debug(result)

    if not os.path.exists(tmp_file) or 'ERROR 404' in result:
        logger.debug('ERROR GETTING: ' + tmp_file)
        raise ValueError
    else:
        logger.debug('Downloaded: ' + os.path.abspath(tmp_file))

    # if test:
    logger.debug(
        '\nMEDIA_PATH:\t%s\nTMP_STOR_DIR:\t%s\nTMP_FILE:\t%s\nABS_DIR:\t%s'
        % (file_path, tmp_stor_dir, tmp_file, absolute_directory))

    return file_path, tmp_stor_dir, tmp_file, absolute_directory