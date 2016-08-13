import os
import imp
import time
import logging
import calendar
import datetime
import itertools
import StringIO

from oss_python_sdk import (
    oss_api, oss_xml_handler, oss_util
)


TZ, SECOND = (8, 1)
MINUTE, HOUR = (60*SECOND, 3600*SECOND)

RETRY_COUNT, RETRY_INTERVAL = (10, 1*SECOND)

DEFAULT_PAGE_SIZE = 500

DEFAULT_THREAD_NUM = 10
MAX_PART_NUM = 10000

def get_logger(test_name):
    log = logging.getLogger(test_name)
    log.setLevel(logging.INFO)
    hdlr = logging.FileHandler(test_name + '.LOG')
    hdlr.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s]\t[%(levelname)s]\t[%(thread)d]\t[%(pathname)s:%(lineno)d]\t%(message)s")
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    return log

global_logger = get_logger('simple_oss')

class OssError(Exception):
    def __init__(self, status, code, err_info):
        super(OssError, self).__init__(self)
        self.st = status
        self.code = code
        self.err = err_info

    def __str__(self):
        return 'status: %s code: %s'%(
            self.get_status(), self.get_code())

    def get_status(self):
        return self.st
   
    def get_code(self):
        return self.code

class OssUnretryError(OssError):
    def __init__(self, status, code, err_info):
        self.st = status
        self.code = code
        self.err = err_info
        super(OssUnretryError, self).__init__(self.st, self.code, self.err)
       
class ObjectNotExists(OssUnretryError):
    def __init__(self, status, code, err_info):
        self.st = status
        self.code = code
        self.err = err_info
        super(ObjectNotExists, self).__init__(self.st, self.code, self.err)

class InvalidBucket(OssUnretryError):
    def __init__(self):
        self.st = 403
        self.code = 'AccessDenied'
        self.err = 'Bucket is unaccessable'
        super(ObjectNotExists, self).__init__(self.st, self.code, self.err)

def oss_to_epoch(timestamp):
    # given a time string like: 2014-05-15T11:18:32.000Z
    # convert it to an epoch time.
    imp.acquire_lock()
    ts = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.000Z").timetuple()
    imp.release_lock()
    return (int)(time.mktime(ts))

def gmt_to_epoch(gmtT):
    return (int)(calendar.timegm(time.strptime(gmtT, "%a, %d %b %Y %H:%M:%S GMT")))

class CheckWrapper(object):
    def __init__(self):
        pass

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            res = self.do_check(response)
            return res
        return wrapper

    def do_check(self, http_response):
        data, status = http_response.read(), http_response.status
        if status/100 == 2:
            error = None
        elif status == 403:
            error = oss_xml_handler.ErrorXml(data)
            raise OssUnretryError(403, error.code, error)
        elif status == 404:
            error = oss_xml_handler.ErrorXml(data) 
            raise ObjectNotExists(404, error.code, error)
        else:
            error = oss_xml_handler.ErrorXml(data)
            raise OssError(status, error.code, error)
        return ResponseProxy(http_response, data, error)

class RetryWrapper(object):
    def __init__(self, verbose):
        self.verbose = verbose
        self.retry, self.interval = (RETRY_COUNT, RETRY_INTERVAL)
        self.log_action = global_logger.info

    def do_log(self, retry_times):
        retry_info = 'Retry times: %d.'%(retry_times, ) if retry_times else 'No retry.'
        logs = [self.status_prompt, self.prompt, retry_info]
        self.log_action(''.join(logs))
       
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            error = None
            self.status_prompt = 'Try to '
            self.prompt = '''calling %s(args=%s, kwargs=%s) '''%(func.__name__, args[1:], kwargs)
            for retried in range(self.retry):
                try:
                    if error: time.sleep(self.interval)
                    result = func(*args, **kwargs)
                except OssUnretryError, e:
                    error = e
                    raise e
                except OssError, e:
                    error = e
                    continue
                except Exception, e:
                    error = e
                    continue
                else:
                    error = None
                    return result
                finally:
                    if error:
                        self.status_prompt = 'Failed to '
                        self.log_action = global_logger.exception
                    else:
                        self.status_prompt = 'Successed to '
                        self.log_action = global_logger.info
                    if self.verbose: self.do_log(retried)
            else:
                if error: raise error
        return wrapper

    def set_verbose(self):
        self.verbose = True

    def clear_verbose(self):
        self.verbose = False

    def set_retry(self, retry, interval):
        self.retry, self.interval = (retry, interval)

class OssAPIProxy(object):
    def __init__(self, host, id, key):
        self.oss = oss_api.OssAPI(host, id, key)
        self.check_wrapper = CheckWrapper()

    def __getattr__(self, attr):
        if attr == 'head_object':
            origin_method = self.head_object
        else:
            origin_method = getattr(self.oss, attr)
        return self.check_wrapper(origin_method)

    def head_object(self, bucket, path):
        h = {'Range': 'bytes=0-0'}
        response = self.oss.head_object(bucket, path)
        response.read()
        body = self.get_object(bucket, path, headers=h)
        return ResponseProxy(response, body.read())

    def get_all_buckets(self):
        marker = ""
        prefix = ""
        headers = None

        buckets = []
        while True:
            res = self.oss.get_service(headers, prefix, marker)
            body = res.read()
            (bucket_meta_list, marker) = oss_util.get_bucket_meta_list_marker_from_xml(body)
            for i in bucket_meta_list:
                buckets.append(str(i.name))
            if not marker:
                break;
        return buckets

class ResponseProxy(object):
    def __init__(self, response, data, error=None):
        self.response = response
        self.error = error
        self.data = StringIO.StringIO()
        self.data.write(data)
        self.data.seek(0)

    def __getattr__(self, attr):
        if attr == 'read':
            return self.data.read
        else:
            return getattr(self.response, attr)

class MetaClass(type):
    def __new__(cls, nm, parents, attrs):
        super_new = super(MetaClass, cls).__new__
        retry_wrapper = RetryWrapper(attrs.get('verbose'))
        for key, value in attrs.iteritems():
            if callable(value) and not key.startswith('__'):
                attrs[key] = retry_wrapper(value)
            else:
                pass
        attrs['retry_wrapper'] = retry_wrapper
        return super_new(cls, nm, parents, attrs)

class SimpleOss(object):

    __metaclass__ = MetaClass
    verbose = False

    def __init__(self, *args, **kwargs):
        meta_keys = ['host', 'id', 'key']
        metas = map(kwargs.get, meta_keys)
        if None in metas:
            metas = args[:3]
        self.clnt = OssAPIProxy(*metas)

    def set_verbose(self):
        self.retry_wrapper.set_verbose()

    def clear_verbose(self):
        self.retry_wrapper.clear_verbose()

    def set_retry(self, retry, interval):
        self.retry_wrapper.set_retry(retry, interval)

    def list(self, bucket, dir, delimiter='', verbose=False):
        page_size = DEFAULT_PAGE_SIZE
        xml_hdlr = oss_xml_handler
        def next_page():
            next_marker = ''
            is_truncated = True
            while is_truncated:
                res = self.clnt.get_bucket(bucket, dir,
                            next_marker, delimiter, page_size)
                parsed_xml = xml_hdlr.GetBucketXml(res.read())
                entry_list = parsed_xml.content_list
                prefix_list = parsed_xml.prefix_list
                for entry in itertools.chain(prefix_list, entry_list):
                    if isinstance(entry, (str, unicode)):
                        yield str(entry)
                    else:
                        yield (entry.key, entry.size, oss_to_epoch(entry.last_modified)) \
                            if verbose else str(entry.key)
                else:
                    is_truncated = parsed_xml.is_truncated
                    next_marker = parsed_xml.nextmarker
        l = [entry for entry in next_page()]
        return l

    def upload(self, bucket, file, object):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        op = os.path
        if op.isdir(file):
            file = op.join(file, op.basename(object))
        res = self.clnt.put_object_from_file(bucket, object, file)
        return not res.error

    def download(self, bucket, file,object):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        op = os.path
        if op.isdir(file):
            file = op.join(file, op.basename(object))
        res = self.clnt.get_object_to_file(bucket, object, file)
        return not res.error

    def delete(self, bucket, path):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        if self.isdir(bucket, path):
            for object in self.list(bucket,path):
                self.clnt.delete_object(bucket, object)
        else:
            self.clnt.delete_object(bucket, path)
        return True

    def exists(self, bucket, path):
        if not path or path.endswith('/'):
            res = self.clnt.get_bucket(bucket, path)
            parsed_xml = oss_xml_handler.GetBucketXml(res.read())
            return True if parsed_xml.content_list else False
        else:
            try:
                res = self.clnt.head_object(bucket, path)
                return True
            except ObjectNotExists:
                return False

    def isdir(self, bucket, path):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        if not path.endswith(os.sep):
            path += os.sep
        if self.exists(bucket, path):
            next_marker = ''
            delimiter = ''
            page_size = 1
            res = self.clnt.get_bucket(bucket, path,
                                next_marker, delimiter, page_size)
            parsed_xml = oss_xml_handler.GetBucketXml(res.read())
            if parsed_xml.is_truncated or len(parsed_xml.content_list)>=1:
                return True
            else:
                return False
        else:
            return False

    def download_str(self, bucket, path):
        res = self.clnt.get_object(bucket, path)
        return res.read()

    def upload_str(self, bucket, str1, path):
        res = self.clnt.put_object_from_string(bucket, path, str1)
        return not res.error

    def list_bucket(self, verbose=False):
        res = self.clnt.list_all_my_buckets()
        parsed_xml = oss_xml_handler.GetServiceXml(res.read())
        buckets = [bkt_info if verbose else bkt_info[0] for bkt_info in parsed_xml.list()]
        return buckets

    def len(self, bucket, path):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        len, _, _ = self.stat(bucket, path)
        return len

    def stat(self, bucket, path):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        res = self.clnt.head_object(bucket, path)
        len = int(res.getheader('content-length'))
        etag = res.getheader('etag')
        mtime = gmt_to_epoch(res.getheader('last-modified'))
        return len, etag, mtime

    def multi_get(self, bucket, object, file, thread=DEFAULT_THREAD_NUM):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        if file.endswith('/'):
            file = os.path.join(file, os.path.basename(object))
        return oss_util.multi_get(self.clnt, bucket,
                object, file, thread, RETRY_COUNT)

    def multi_put(self, bucket, file, object, thread=DEFAULT_THREAD_NUM):
        if str(bucket) not in self.clnt.get_all_buckets():
            raise InvalidBucket()

        id, part_num, h = ('', MAX_PART_NUM, {})
        res = self.clnt.multi_upload_file(bucket, object, file,
                id, thread, part_num, h)
        return not res.error
