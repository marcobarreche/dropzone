# -*- coding: utf-8 -*-
#
# http://docs.aws.amazon.com/AmazonS3/latest/dev/LogFormat.html
# Log Format:
# bucket_owner = The canonical user id of the owner of the source bucket.
# bucket = The name of the bucket that the request was processed against. If the system receives a
#          malformed request and cannot determine the bucket, the request will not appear in any
#          server access log.
# time = The time at which the request was received. The format, using strftime() terminology, is
#        [%d/%b/%Y:%H:%M:%S %z]
# remote_ip = The apparent Internet address of the requester. Intermediate proxies and firewalls
#             might obscure the actual address of the machine making the request
# requester = The canonical user id of the requester, or the string "Anonymous" for unauthenticated
#             requests. This identifier is the same one used for access control purposes
# request_id = The request ID is a string generated by Amazon S3 to uniquely identify each request
# operation = Either SOAP.operation, REST.HTTP_method.resource_type or
#             WEBSITE.HTTP_method.resource_type
#       Ex.
#       REST.POST.BUCKET -- upload
#       REST.OPTIONS.PREFLIGHT -- ensure if a Put request can be commited
#       REST.PUT.OBJECT -- Add logs
#       REST.DELETE.OBJECT -- Remove object
# key = The "key" part of the request, URL encoded, or "-" if the operation does not take a key
#       parameter
# request_uri = The Request-URI part of the HTTP request message
# http_status = The numeric HTTP status code of the response
# error_code = The Amazon S3 Error Code, or "-" if no error occurred
#              (http://docs.aws.amazon.com/AmazonS3/latest/dev/ErrorCode.html)
# bytes_sent = The number of response bytes sent, excluding HTTP protocol overhead, or "-" if zero
# object_size = The total size of the object in question
# total_time = The number of milliseconds the request was in flight from the server's perspective.
#              This value is measured from the time your request is received to the time that the
#              last byte of the response is sent. Measurements made from the client's perspective
#              might be longer due to network latency
# turn_around_time = The number of milliseconds that Amazon S3 spent processing your request.
#                    This value is measured from the time the last byte of your request was
#                    received until the time the first byte of the response was sent
# referrer = The value of the HTTP Referrer header, if present. HTTP user-agents (e.g. browsers)
#            typically set this header to the URL of the linking or embedding page when making a
#            request
# user_agent = The value of the HTTP User-Agent header
# versio_id = The version ID in the request, or "-" if the operation does not take a versionId
#             parameter
#
# Log entry Example:
# 3ddac93e0960f928f9e95184bff23d2cd7229c2c9d1c661f0c741b9eedc4da66 barreche-tb [26/Sep/2013:16:45:54 +0000] 10.87.133.107 3ddac93e0960f928f9e95184bff23d2cd7229c2c9d1c661f0c741b9eedc4da66 DDA0909B664CC651 REST.GET.NOTIFICATION - "GET /barreche-tb?notification HTTP/1.1" 200 - 115 - 67 - "-" "S3Console/0.4" -
#

from boto.s3.connection import S3Connection
from collections import namedtuple
from functools import wraps
import csv
import datetime
import logging
import os
import time
import sys


SERVICE_S3 = {
    'access_key': 'AKIAIM7RS3YPLGU2I6YQ',
    'secret_key': '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',
    'bucket_name': 'barreche-tb',
    'path-logs': '/logs/',
    'path-uploads': '/uploads/'
}
logging.basicConfig(level=logging.DEBUG)
LOG_FILE_LOCAL_DIR = "local-logs/"
LogEntry = namedtuple('LogEntry', 'bucket_owner bucket time remote_ip requester request_id '
                                  'operation key request_uri http_status error_code bytes_sent '
                                  'object_size total_time turn_around_time referrer user_agent '
                                  'versio_id'.split())


def create_request_list_objects(local_folder, date=None, debug=False):
    """
    Download all the files inside the folder s3_folder and download all files into local_folder.

    Arguments:
        local_folder (str): The local folder where the files will be saved. It must end in '/'.
        date (datetime.datetime): Optional. If you specify a date, only the all logs after this
                                            date will be download.
        debug (boolean): Optional. True if you want to see what happens inside the function.
                                   False, otherwise

    Returns:
        (None | datetime.datetime): The datetime of the last log or None if there is not any log in s3.
    """
    conn = S3Connection(SERVICE_S3.get('access_key'), SERVICE_S3.get('secret_key'))
    mybucket = conn.get_bucket(SERVICE_S3.get('bucket_name'), validate=False)
    path = SERVICE_S3.get('path-logs')[1:]
    last_modified = None
    for key in mybucket.list():
        if not (key.name).startswith(path):
            continue
        date_key = datetime.datetime.strptime(key.last_modified, '%Y-%m-%dT%H:%M:%S.000Z')
        if date and date > date_key:
            continue
        filename = '%s%s.txt' % (local_folder, key.name.split('/')[-1])
        if debug:
            logging.debug('Create file: %s, [%s]', filename, key.last_modified)
        key.get_contents_to_filename(filename)
        last_modified = date_key
    return last_modified


def delete_list_objects_before_date(date=None, debug=False):
    """
    Delete all logs older than a specific date from the s3 bucket.

    Arguments:
        date (datetime.datetime): Optional. If you don't specify a date, all logs will be deleted.
        debug (boolean): Optional. True if you want to see what happens inside the function.
                                   False, otherwise
    """
    conn = S3Connection(SERVICE_S3.get('access_key'),
                        SERVICE_S3.get('secret_key'))
    mybucket = conn.get_bucket(SERVICE_S3.get('bucket_name'), validate=False)
    path = SERVICE_S3.get('path-logs')[1:]
    for key in mybucket.list():
        if not (key.name).startswith(path):
            continue
        date_key = datetime.datetime.strptime(key.last_modified, '%Y-%m-%dT%H:%M:%S.000Z')
        if date and date > date_key:
            continue
        filename = key.name
        key.delete()
        if debug:
            logging.debug('Delete file: %s', filename)


def timed(f):
    """Wrapper to show for how long does a function run."""
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.time()
        result = f(*args, **kwds)
        elapsed = time.time() - start
        now_ts = datetime.datetime.now()
        print '%s - %s took %d seconds to finish.' % (now_ts, f.__name__, elapsed)
        return result
    return wrapper


@timed
def parser():
    s3_billing = {}
    try:
        logging.debug('Starting Amazon S3 log parser...')
        files = get_files_from_path(LOG_FILE_LOCAL_DIR)

        logging.debug('Parsing %s log files', len(files))
        for fname in files:
            logging.debug('Parsing log file %s', fname)
            log_entries = get_s3_log_entries(absolute_file_path(LOG_FILE_LOCAL_DIR, fname))

            logging.debug('[%s] entries on this log file', len(log_entries))
            entries_objects = parse_all_s3_log_entries(log_entries)

            logging.debug('Filtering the entries ...')
            s3_billing = filter_valid_operations(entries_objects, s3_billing)

            logging.debug('Storing entry objects...')
            store_entries(s3_billing)
    except Exception, e:  # pylint: disable=W0703
        logging.exception('Error parsing S3 logs: %s', str(e))
        logging.exception('Commmand: %s', absolute_file_path(LOG_FILE_LOCAL_DIR, fname))
    logging.debug('Amazon S3 log parser ends.')


def filter_valid_operations(list_operations, s3_billing):
    """We remove all operations over this key /bucket-name/logs/*"""
    for operations in list_operations:
        path = '/%s' % operations.key   # Example operations.key = uploads/marco/p.png

        # First Filter
        if not path.startswith(SERVICE_S3['path-uploads']):
            continue

        # Second Filter
        if operations.operation.split('.')[1] == 'DELETE':  # Example operations.operation = REST.DELETE.OBJECT
            continue

        # Update billing
        api_key = path[len(SERVICE_S3['path-uploads']):].split('/')[0]
        s3_billing[api_key] = update_billings(api_key, s3_billing, operations)

    return s3_billing


def update_billings(api_key, s3_billing, operations):  
    bill = s3_billing.get(api_key)

    # Create bill
    if not bill:
        bill = {
            'entries': [],
            'POST': {
                'counter-request': 0,
                'counter-bw': 0
            },
            'GET': {
                'counter-request': 0,
                'counter-bw': 0
            },
            'OTHER': {
                'counter-request': 0,
                'counter-bw': 0
            }
        }

    # Update bill
    bill['entries'].append(operations)

    method = operations.operation.split('.')[1]  # Example: operations.operation = REST.PUT.ACL
    if method not in ('GET', 'POST'):
        method = 'OTHER'

    bill[method]['counter-request'] += 1
    if operations.bytes_sent != '-':
        bill[method]['counter-bw'] += int(operations.bytes_sent)
    if operations.object_size != '-':
        bill[method]['counter-bw'] += int(operations.object_size)
    return bill


def is_file(PATH, filename):
    """Is PATH/filename a file?. """
    return os.path.isfile(os.path.join(PATH, filename)) and filename.endswith('.txt')


def get_files_from_path(PATH):
    """Get all files from PATH"""
    return [f for f in os.listdir(PATH) if is_file(PATH, f)]


def absolute_file_path(PATH, filename):
    """Returns the absolute filename PATH/filename"""
    return os.path.join(PATH, filename)


def get_s3_log_entries(log_file):
    """Get all log entries."""
    log_entries = []

    with open(log_file) as f:
        r = csv.reader(f, delimiter=' ',quotechar='"')
        if not r:
            return []
        for i in r:
            i[2] = i[2] + " " + i[3] # repair date field
            del i[3]
            log_entries.append(i)
    return log_entries


def parse_all_s3_log_entries(log_entries):
    for e in log_entries:
        yield parse_s3_log_entry(e)


def parse_s3_log_entry(entry):
    return LogEntry._make(entry)


def store_entries(entries):
    # TODO: Store where?
    pass
    # db_entries = [(entry.bucket_owner, ...) for entry in entries]

    # with closing(dbdriver.connect(**DB_OPTS)) as db:
    #     for db_entries_group in utils.ibuckets(db_entries, 200):
    #         with closing(db.cursor()) as c:
    #             c.executemany("""
    #               INSERT INTO table_name (x1, x2, x3)
    #               VALUES (v1, v2, v3)
    #               ON DUPLICATE KEY UPDATE x4=v4
    #               """, db_entries_group)
    #         db.commit()


def bill_to_string(bill):
    res = ''
    for api_key in bill:
        obj = bill[api_key]

        entries = ''
        for entry in obj.get('entries'):
            entries += entry_to_string(entry)

        res += """%s >> [\n\tPOST = {count: %d, bw: %d}, GET = {count: %d, bw: %d}, OTHER = {count: %d, bw: %d}
            Entries: \n\t[\n%s]\n]""" % (
                api_key, int(obj['POST']['counter-request']),
                int(obj['POST']['counter-bw']), int(obj['GET']['counter-request']),
                int(obj['GET']['counter-bw']), int(obj['OTHER']['counter-request']),
                int(obj['OTHER']['counter-bw']), entries)
    return res


def entry_to_string(entry):
    return """\t\t[%s %s, "%s": http_status: %s, error_code: %s, bytes_sent: %s, object_size: %s, total_time: %s]\n""" % (
        entry.operation, entry.key, entry.request_uri, entry.http_status, entry.error_code,
        entry.bytes_sent, entry.object_size, entry.total_time)


if __name__ == '__main__':
    try:
        option = sys.argv[1]
        if option == '--op':
            function = sys.argv[2]
            if function == 'download':
                date = None
                if len(sys.argv) > 4:
                    date = sys.argv[4]
                create_request_list_objects(sys.argv[3], date=date, debug=True)
            elif function == 'delete':
                date = None
                if len(sys.argv) > 3:
                    date = sys.argv[3]
                delete_list_objects_before_date(date=date, debug=True)
            elif function == 'parser':
                parser()
    except IndexError:
        print 'python logs_downloader.py --op download name_folder [date]'
        print 'python logs_downloader.py --op delete [date]'
        print 'python logs_downloader.py --op parser'
