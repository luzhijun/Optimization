'''Definition of most of exceptions type across BatchCompute SDK.
'''

class ClientError(Exception):
    def __init__(self, code, request_id, msg):
        self.code = code
        self.request_id = request_id
        self.msg = msg

    def get_code(self):
        return self.code

    def get_requestid(self):
        return self.request_id

    def get_msg(self):
        return self.msg

    def __str__(self):
        return 'Code: %s, RequestID: %s, Message: %s'%(
            self.code, self.request_id, self.msg)

class FieldError(Exception):
    def __init__(self, key):
        super(FieldError, self).__init__()
        self._k = key

    def __str__(self):
        return key

class ValidationError(Exception):
    def __init__(self, key):
        super(ValidationError, self).__init__()
        self._k = key

    def __str__(self):
        return self._k

class JsonError(Exception):
    def __init__(self, msg):
        super(JsonError, self).__init__(msg)
