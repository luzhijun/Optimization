'''Implementation of jsonizable Job, Task, Instance, Image and four types
responses of BatchComputeClient service.
'''

from batchcompute.utils import CamelCasedClass, remap, add_metaclass
from batchcompute.utils.jsonizable import Jsonizable, BatchEncoder
from batchcompute.utils.constants import STRING, NUMBER, TIME, PY2, PY3
from batchcompute.utils.functions import import_json

json = import_json()

########################
#RESOURCES STATUS CLASS#
########################

class Job(Jsonizable):
    descriptor_type = 'non data descriptor'
    descriptor_map = {
        'JobId': STRING,
        'JobName': STRING,
        'Description': STRING,
        'Priority': NUMBER,
        'State': STRING,
        'OwnerId': NUMBER,
        'CreateTime': TIME,
        'StartTime': TIME,
        'EndTime': TIME,
        'TotalTime': TIME,
        'NumTotalTask': NUMBER,
        'NumFinishedTask': NUMBER,
        'NumFailedTask': NUMBER,
        'NumWaitingTask': NUMBER,
        'NumRunningTask': NUMBER,
        'NumStoppedTask': NUMBER,
        'NumTotalInstance': NUMBER,
        'NumFinishedInstance': NUMBER,
        'NumFailedInstance': NUMBER,
        'NumWaitingInstance': NUMBER,
        'NumRunningInstance': NUMBER,
        'NumStoppedInstance': NUMBER,
    }

    def __init__(self, dct):
        super(Job, self).__init__(dct)

    if PY2:
        def __cmp__(self, other):
            '''
            Used as method to sort a collection of Job in Python 2.

            Build-in functions `cmp` and `__cmp__` were deprecated since Python
            3.
            '''
            if isinstance(other, self.descriptor_map['JobId']):
                other_job_id = other
            else:
                other_job_id = other['JobId']
            return cmp(self['JobId'], other_job_id)

    if PY3:
        def __lt__(self, other):
            '''
            Used as method to sort a collection of Job in Python 3.
            '''
            if isinstance(other, self.descriptor_map['JobId']):
                other_job_id = other
            else:
                other_job_id = other.JobId
            return self.JobId < other_job_id


class Task(Jsonizable):
    descriptor_type = 'non data descriptor'
    descriptor_map = {
        'TaskName': STRING,
        'State': STRING,
        'StartTime': TIME,
        'EndTime': TIME,
        'InstanceList': list,
    }

    def __init__(self, dct):
        super(Task, self).__init__(dct)

    def setproperty(self, key, value):
        super_set = super(Task, self).setproperty
        if key == 'InstanceList' and isinstance(value, list):
            InstanceList = []
            for instance in value:
                InstanceList.append(Instance(instance))
            new_value = InstanceList
        else:
            new_value = value
        super_set(key, new_value)

    if PY2:
        def __cmp__(self, other):
            lh = (self.StartTime, self.TaskName)
            rh = (other.StartTime, other.TaskName)
            return cmp(lh, rh)

    if PY3:
        def __lt__(self, other):
            lh = (self.StartTime, self.TaskName)
            rh = (other.StartTime, other.TaskName)
            return lh < rh


class Image(Jsonizable):
    descriptor_type = 'non data descriptor'
    descriptor_map = {
        'Platform': STRING,
        'ImageName': STRING,
        'Description': STRING,
        'ImageId': STRING,
    }

    def __init__(self, dct):
        super(Image, self).__init__(dct)

    if PY2:
        def __cmp__(self, other):
            if isinstance(other, self.descriptor_map['ImageId']):
                other_image_id = other
            else:
                other_image_id = other['ImageId']
            return cmp(self['ImageId'], other_image_id)

    if PY3:
        def __lt__(self, other):
            if isinstance(other, self.descriptor_map['ImageId']):
                other_image_id = other
            else:
                other_image_id = other['ImageId']
            return self['ImageId'] < other_image_id

class Instance(Jsonizable):
    descriptor_type = 'non data descriptor'
    descriptor_map = {
        'InstanceId': NUMBER,
        'State': STRING,
        'StartTime': TIME,
        'EndTime': TIME,
    }

    def __init__(self, dct):
        super(Instance, self).__init__(dct)

    if PY2:
        def __cmp__(self, other):
            if isinstance(other, self.descriptor_map['InstanceId']):
                other_instance_id = other
            else:
                other_instance_id = other['InstanceId']
            return cmp(self['InstanceId'], other_instance_id)

    if PY3:
        def __lt__(self, other):
            if isinstance(other, self.descriptor_map['InstanceId']):
                other_instance_id = other
            else:
                other_instance_id = other['InstanceId']
            return self['InstanceId'] < other_instance_id

# Add CamelCasedClass metaclass to all resource status classes.
Job = add_metaclass(Job, CamelCasedClass)
Task = add_metaclass(Task, CamelCasedClass)
Instance = add_metaclass(Instance, CamelCasedClass)
Image = add_metaclass(Image, CamelCasedClass)


################
#RESPONSE CLASS#
################

class RawResponse(object):
    '''
    Base class for all client response subclasses.

    Mainly suppulys `StatusCode`, `RequestId` and `Date` property and methods
    to retrive them.

    '''
    descriptor_type = 'non data descriptor'
    descriptor_map = {
        'StatusCode': NUMBER,
        'RequestId': STRING,
        'Date': STRING,
    }

    def __init__(self, response, human_readable):
        self._d = {}

        self.setproperty('StatusCode', response.status)
        self.setproperty('RequestId', response.getheader('request-id'))
        self.setproperty('Date', response.getheader('date'))

        self.content = remap(response.read(), human_readable)

    def getproperty(self, key):
        return self._d[key]

    def setproperty(self, key, value):
        if key in self.descriptor_map:
            if isinstance(value, self.descriptor_map[key]):
                self._d[key] = value
            else:
                raise TypeError('Property %s must be type of %s'%(key,
                                str(self.descriptor_map[key])))
RawResponse = add_metaclass(RawResponse, CamelCasedClass)


class CreateResponse(RawResponse):
    descriptor_type = 'non data descriptor'
    descriptor_map = {
        'JobId': STRING,
    }

    def __init__(self, response, human_readable):
        super(CreateResponse, self).__init__(response, human_readable)
        self.setproperty('JobId', self.content['JobId'])

    def __str__(self):
        d = {'JobId': self._d['JobId']}
        return json.dumps(d, indent=4)
CreateResponse = add_metaclass(CreateResponse, CamelCasedClass)


class ActionResponse(RawResponse):
    '''
    Response for operations on jobs(Stop, Start, delete).
    '''
    def __init__(self, response, human_readable):
        super(ActionResponse, self).__init__(response, human_readable)


class GetResponse(RawResponse):
    '''
    Response for get operations on jobs, tasks or images.
    '''
    def __init__(self, response, type_, human_readable):
        super(GetResponse, self).__init__(response, human_readable)
        # Instantiation the real resource status class with the http body(
        # usually a json formatted string) returned by BatchCompute service.
        self._container = type_(self.content)

    def __getattr__(self, attr):
        return getattr(self._container, attr)

    if PY2:
        def __str__(self):
            return self._container.__str__()

    if PY3:
        def __bytes__(self):
            return self.__container.__str__()

    def __repr__(self):
        return self.__str__()


class ListResponse(RawResponse):
    def __init__(self, response, type_, human_readable):
        super(ListResponse, self).__init__(response, human_readable)
        # Http body returned by BatchCompute service for list requests usually
        # a json formatted dict object, but response will be converted to a
        # list-like object sorted according to `__cmp__`(Python 2) or `__lt__`
        # (Python 3) method of `type_` class instance.
        self._container = sorted(map(type_, self.content.values()))

    def __getattr__(self, attr):
        return getattr(self._container, attr)

    def __iter__(self):
        return iter(self._container)

    def __getitem__(self, index_or_slice):
        return self._container[index_or_slice]

    def __len__(self):
        return len(self._container)

    def __str__(self):
        return json.dumps(self._container, indent=4, cls=BatchEncoder)
