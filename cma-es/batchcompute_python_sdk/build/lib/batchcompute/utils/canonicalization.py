'''
Functions and classes to make interfaces or keys canonicalization.
'''
import re
from datetime import timedelta

from .functions import partial, timestamp_datetime, import_json, timediff
from .constants import STATE_MAP, PY2, PY3, STRING
# from batchcompute.core.exceptions import JsonError

json = import_json()

"""
def lower_camel_case(name):
    '''
    Make parameter 'name' conform to lower camel case convention.

    Exp:
        State --> state, get_state --> getState
        StartTime --> startTime, get_start_time --> getStartTime
    '''
    sep = '_'

    def add_underline(matched):
        '''
        An function used as 'repl' parameter of the method:
        re.sub(pattern, repl, string, count=0, flags=0).
        '''
        uppercase = matched.group('uppercase')
        return sep + uppercase.lower()

    def to_underlined(s):
        '''
        Add underline before each uppercase in a str before convert all.
        uppercases to lowercases.
        '''
        pattern = '(?P<uppercase>[A-Z])'
        underlined_cases = re.sub(pattern, add_underline, name)
        return underlined_cases.strip(sep)

    # Split name with `_`.
    words = to_underlined(name).split('_')
    # Capitalize all except the first word.
    cameled_words = [word.capitalize() if index != 0 else word \
                     for index, word in enumerate(words)]
    return ''.join(cameled_words)
"""

class CamelCasedClass(type):
    '''
    MetaClass for all classes which expected supply lower-camel-case methods
    instead of methods with `_` joined lower cases.

    Mainly add descriptor for each property descripted in description dict.

    e.g.:
        You can get JobId of a job status 'j' through both j.jobId and
        j.getJobId(), and the like.

    '''
    def __new__(cls, nm, parents, attrs):
        super_new = super(CamelCasedClass, cls).__new__

        tmp_dct = dict()
        for name, value in attrs.items():
            if not name.startswith('__') and not name.endswith('__'):
                tmp_dct[name] = value
        attrs.update(tmp_dct)

        # Create property for each key in `description_map` dict.
        # Besides, if `descriptor_type` is data descriptor, a `getxxx` and
        # a `setxxx` method also will be added to `cls`, if `descriptor_type`
        # is non data descriptor, only a `getxxx` method added.
        if 'descriptor_map' in attrs:
            for attr in attrs['descriptor_map']:
                # Definition of getter and setter method for properties.
                def get_attr(attr, self):
                    return self.getproperty(attr)
                def set_attr(attr, self, value):
                    self.setproperty(attr, value)

                property_name = attr
                getter = partial(get_attr, attr)
                setter = partial(set_attr, attr)
                # Add property to class.
                if attrs['descriptor_type'] == 'data descriptor':
                    # data descriptor.
                    attrs[property_name] = property(getter, setter, None, attr)
                else:
                    # non data descriptor.
                    attrs[property_name] = property(getter, None, None, attr)
        return super_new(cls, nm, parents, attrs)


def remap(container, human_readable=False):
    '''
    Canonicalize keys in container to standard names.

    `container` must be a list, dict or string.
    '''
    if not container:
        return dict()

    if PY2:
        if isinstance(container, str):
            s = container.strip()
            container = json.loads(container) if s else dict()
    else:
        # For Python 3 compatibility.
        if isinstance(container, bytes):
            s = str(container, encoding='ascii').strip()
            container = json.loads(s) if s else dict()

    new_container = type(container)()
    if isinstance(container, dict):
        if 'Name' in container:
            if container['ResourceId'].startswith('job-'):
                new_container['JobName'] = container['Name']
            else:
                new_container['ImageName'] = container['Name']
            del container['Name']
        if 'ResourceId' in container:
            if container['ResourceId'].startswith('job-'):
                new_container['JobId'] = container['ResourceId']
            else:
                new_container['ImageId'] = container['ResourceId']
            del container['ResourceId']
        if 'State' in container:
            state = 'Finished' if container['State']=='Terminated' \
                    else container['State']
            if isinstance(state, int):
                state = STATE_MAP[container['State']]
            new_container['State'] = state
            del container['State']
        if 'ErrorCode' in container:
            new_container['Code'] = container['ErrorCode']
            del container['ErrorCode']
        if 'InstanceStatusVector' in container:
            new_container['InstanceList'] = container['InstanceStatusVector']
            del container['InstanceStatusVector']
        new_container.update(container)
    else:
        new_container = container

    get_iter = lambda c: c.items() if isinstance(c, dict) else enumerate(c)
    # Make all keys canonical recursively.
    for key, value in get_iter(new_container):
        # XXX maybe unicode
        collection_type = (dict, list)
        if isinstance(value, collection_type):
            if 'UnfinishedInstances' in value:
                # Add TaskName to task status.
                value['TaskName'] = key
            # Dealing with dict and list type recursively.
            new_value = remap(value, human_readable)
        elif human_readable and isinstance(key, STRING) and key.endswith('Time'):
            # Convert epoch time to human readable time format.
            if key == 'TotalTime':
                new_value = timediff(value)
            else:
                new_value = timestamp_datetime(value)
        else:
            new_value = value
        new_container[key] = new_value
    return new_container
