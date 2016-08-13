import sys
import uuid
import base64
import hmac
from hashlib import sha1 as sha

from batchcompute.utils import (
    RequestClient, str_md5, utf8, iget, gmt_time, import_json, get_region,
)
from batchcompute.utils.constants import SERVICE_PORT, API_VERSION, PY2, PY3

json = import_json()

class Api(object):
    '''
    A simple api implemention for batch compute, which supply operations for
    users to connect to BatchCompute service.
    '''
    prefix = 'x-acs-'
    version = API_VERSION

    def __init__(self, endpoint, access_id, secret_key):
        self.endpoint = endpoint
        self.host, self.port = endpoint, SERVICE_PORT
        self.id, self.key = (access_id, secret_key)

        self.accept = 'application/json'
        self.content_type = 'text/html'

        self.sign_method = 'HMAC-SHA1'
        self.sign_version = '1.0'

        self.provider = 'acs'
        self.rc = RequestClient(self.host, self.port)

        self.url_sep = '/'

    def raw_headers(self, body):
        '''
        Headers without 'Authorization' key-value pair.
        '''
        date = gmt_time()
        h = dict()
        h['Date'] = date
        h['x-acs-region-id'] = get_region(self.endpoint)
        h['x-acs-access-key-id'] = self.id
        h['x-acs-signature-method'] = self.sign_method
        h['x-acs-signature-version'] = self.sign_version
        h['x-acs-version'] = self.version
        h['x-acs-signature-nonce'] = str(uuid.uuid1())
        h['Accept'] = self.accept
        h['Content-Type'] = self.content_type
        h['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1)'
        if body:
            h['contentMd5'] = str_md5(body)
            h['Content-Length'] = len(body)
        else:
            h['Content-Length'] = 0
        return h

    def get_auth(self, method, path='', params={}, body='', headers={}):
        '''
        Provides an implemention to signature user's http request.

        Returns the signatured string which will be included in the http
        request headers for BatchCompute to identify users.
        '''
        def normalize(url, h):
            '''
            To join all key-value pairs whose key starts with `self.prefix`
            in http headers.
            '''
            _ = lambda s: s.lower().strip()
            assert_prefix = lambda k: _(k).startswith(self.prefix)
            pairs = ['%s:%s\n'%(_(k), utf8(h[k])) for k in
                sorted(h.keys()) if assert_prefix(k)]
            return ''.join(pairs) + url

        h = headers
        md5, type_ = iget(h, 'Content-MD5'), iget(h, 'Content-Type')
        date, accept = iget(h, 'Date'), iget(h, 'Accept')
        key = utf8(self.key)

        url = self.rc.get_url(path, params)
        canonicalized_part = normalize(url, h)

        # Join all parts(request method, accepted format, body md5, content
        # type, other canonicalized parts).
        _ = lambda s: s.strip()
        meta_info = [method, _(accept), _(md5), _(type_), date, canonicalized_part]
        plain_text = '\n'.join(meta_info)

        # Encoding all joined request information.
        if PY3:
            # Only bytes type can be encoded by hmac and base64 in Python 3.
            key = bytes(key, 'ascii')
            plain_text = bytes(plain_text, 'ascii')
        m = hmac.new(key, plain_text, sha)
        encoded_text = base64.b64encode(m.digest())
        if PY3:
            encoded_text = str(encoded_text, encoding='ascii')
        result = "%s %s:%s"%(self.provider, self.id, encoded_text)
        return result

    def get_headers(self, method, path='', params={}, body=''):
        h = self.raw_headers(body)
        h['Authorization'] = self.get_auth(method, path, params, body, h)
        return h

    def attr_join(self, attrs):
        s = ''
        if isinstance(attrs, str):
            s = attrs
        elif isinstance(attrs, (list, tuple)):
            s = ','.join(attrs)
        else:
            pass
        return s

    def url_join(self, url_list):
        valid_entries = filter(lambda x: x, url_list)
        return self.url_sep + self.url_sep.join(valid_entries)

    def get(self, resource, resource_id='', attrs=''):
        entity_list = [resource, resource_id]
        if attrs: entity_list.append(self.attr_join(attrs))
        path = self.url_join(entity_list)
        params = {}
        h = self.get_headers('GET', path, params)
        res = self.rc.get(path, params, h)
        return res

    def post(self, resource, description):
        entity_list = [resource, ]
        path = self.url_join(entity_list)
        params = {}
        if isinstance(description, dict):
            b = json.dumps(description)
        else:
            b = description
        h = self.get_headers('POST', path, params, b)
        res = self.rc.post(path, params, h, body=b)
        return res

    def put(self, resource, resource_id, attrs='', params={}, body=''):
        entity_list = [resource, resource_id]
        if attrs: entity_list.append(self.attr_join(attrs))
        path = self.url_join(entity_list)
        if isinstance(body, dict):
            b = json.dumps(body)
        else:
            b = body
        h = self.get_headers('PUT', path, params, b)
        res = self.rc.put(path, params, h, b)
        return res

    def delete(self, resource, resource_id):
        entity_list = [resource, resource_id]
        path = self.url_join(entity_list)
        params = {}
        h = self.get_headers('DELETE', path)
        res = self.rc.delete(path, params, h)
        return res
