import datetime

from .constants import STRING
from .functions import partial, url_safe, utf8, import_httplib

httplib = import_httplib()

class RequestClient(object):
    '''
    A simple http client implement.
    '''
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']

    def __init__(self, host, port):
        self.h, self.p = (host, port)
        self.c = httplib.HTTPConnection(self.h, self.p)

    def send_request(self, method, path='', params={}, headers={}, body=''):
        # Start args validate sections.
        assert path and isinstance(path, STRING), 'path must be str and may not be Empty'
        assert not params or isinstance(params, dict), 'params must be dict or None'
        assert not params or isinstance(headers, dict), 'headers must be dict or None'
        if method in ['GET', 'HEAD', 'DELETE']:
            assert not params, 'body is not allowed for method'%(metdod)
        else:
            assert not body or isinstance(body, STRING), 'body must be str or None'
        # Finish args validate sections.

        url = self.get_url(path, params)
        self.c.request(method, url, body, headers)
        res = self.c.getresponse()
        return res

    def __getattr__(self, attr):
        if attr.upper() in self.methods:
            return partial(self.send_request, attr.upper())
        else:
            errs = (self.__class__.__name__, attr)
            raise AttributeError("'%s' object has no attribute '%s'"%errs)

    def get_url(self, path, params):
        '''
        Generates request url according to specified params.
        '''
        p = []
        for (k, v) in params.items():
            k, v = (url_safe(k.replace('_', '-')), url_safe(utf8(v)))
            entry = '%s=%s'%(k, v) if v else '%s'%k
            p.append(entry)
        connector = '&'
        seperator = '?' if p else ''
        return '%s%s%s'%(path, seperator, connector.join(p))
