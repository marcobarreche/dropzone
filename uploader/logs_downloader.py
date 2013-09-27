import datetime
import base64
import hashlib
import hmac
from boto.s3.connection import S3Connection


SERVICE_OPTIONS = {
    's3': {
        'access_key': 'AKIAIM7RS3YPLGU2I6YQ',
        'secret_key': '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',
        'bucket_name': 'barreche-tb',
        'path': '/logs/'
    }
}


def calculate_authorization(string_to_sign, access_key, secret_key):
    return 'AWS %s:%s' % (
        access_key,
        base64.b64encode(hmac.new(secret_key, string_to_sign, hashlib.sha1).digest())
    )


def create_request_list_objects(s3_folder, local_folder, date=None, debug=False):
    """
    Download all the files inside the folder s3_folder and download all files into local_folder.

    Arguments:
        s3_folder (str): The folder in s3. It must start and end in '/'.
        local_folder (str): The local folder where the files will be saved. It must end in '/'.
        date (datetime.datetime): Optional. If you specify a date, only the all logs after this
                                            date will be download.
        debug (boolean): Optional. True if you want to see what happens inside the function.
                                   False, otherwise
    """
    conn = S3Connection(SERVICE_OPTIONS.get('s3').get('access_key'), SERVICE_OPTIONS.get('s3').get('secret_key'))
    mybucket = conn.get_bucket(SERVICE_OPTIONS.get('s3').get('bucket_name'), validate=False)
    path = s3_folder[1:]
    for key in mybucket.list():
        if not (key.name).startswith(path):
            continue
        date_key = datetime.datetime.strptime(key.last_modified, '%Y-%m-%dT%H:%M:%S.000Z')
        if date and date > date_key:
            continue
        filename = '%s%s' % (local_folder, key.name.split('/')[-1])
        if debug:
            print 'Create file: %s, [%s]' % (filename, key.last_modified)
        key.get_contents_to_filename(filename)


def eliminate_list_objects_before_date(s3_folder, date=None, debug=False):
    conn = S3Connection(SERVICE_OPTIONS.get('s3').get('access_key'), SERVICE_OPTIONS.get('s3').get('secret_key'))
    mybucket = conn.get_bucket(SERVICE_OPTIONS.get('s3').get('bucket_name'), validate=False)
    path = s3_folder[1:]
    for key in mybucket.list():
        if not (key.name).startswith(path):
            continue
        date_key = datetime.datetime.strptime(key.last_modified, '%Y-%m-%dT%H:%M:%S.000Z')
        if date and date > date_key:
            continue
        filename = key.name
        key.delete()
        if debug:
            print 'Delete file: %s' % filename
