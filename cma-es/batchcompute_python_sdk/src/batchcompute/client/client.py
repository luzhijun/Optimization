'''Implementation of BatchComputeClient
'''
from functools import wraps

from .response import (
    Job, Task, Image, RawResponse, ListResponse,
    GetResponse, ActionResponse, CreateResponse,
)
from batchcompute.core import Api
from batchcompute.core.exceptions import ClientError
from batchcompute.resources import JobDescription
from batchcompute.utils import CamelCasedClass, remap, add_metaclass
from batchcompute.utils.constants import STRING


################
#HELPER CLASSES#
################

class ResponseChecker(object):
    '''
    A decorator class to check http response returned by BatchCompute Api.

    If status code of the response returned by a method is not 2xx, it will
    raise an exception with information given by BatchCompute Api about the
    error code, request id, error message for this bad request.

    `human_readable` has the same meanning as parameter of `Client`.

    '''
    def __init__(self, human_readable=False):
        self._h = human_readable

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            raw_response = f(*args, **kwargs)
            return self._check(raw_response)
        return wrapper

    def _check(self, response):
        '''
        Concrete method to do status code checking of the http response.
        '''
        status = response.status
        if status//100 == 2:
            return response
        else:
            # Determining errors according to the status code of the response,
            # if the error code is not 2xx, we will parse error code, request
            # id and error message from the body returned from BatchCompute
            # service, recording them in a ClientError exception and raise it.
            error = remap(response.read(), self._h)
            request_id = response.getheader('request-id')
            raise ClientError(error['Code'], request_id, error['Message'])


class CheckedApi(object):
    '''
    A proxy class to add error checking response of each api invocation.
    '''
    def __init__(self, region, access_key_id, access_key_secret, human_readable=False):
        self._c = Api(region, access_key_id, access_key_secret)
        self._check = ResponseChecker(human_readable)

    def __getattr__(self, attr):
        methods_to_check = [
            'post',
            'put',
            'get',
            'get',
            'delete',
        ]
        raw_method = getattr(self._c, attr)
        if attr in methods_to_check:
            method = self._check(raw_method)
        else:
            method = raw_method
        return method


#####################
#BatchCompute Client#
#####################

class Client(object):
    '''
    A simple client to use BatchCompute service.

    If `human_readable` is True, some information in response will be formatted
    for more readability, otherwise, the client will not make this effort.

    For example:
        '2015-05-04 17:55:29'(str) is more human readable for time format, but
        1430733329(int), which is a epoch time, is more general for programer.

    '''

    def __init__(self, region, access_key_id, access_key_secret, human_readable=False):
        self._h= human_readable
        self._sa = CheckedApi(region, access_key_id, access_key_secret, self._h)

    def _get_id(self, job):
        if isinstance(job, CreateResponse):
            job_id = job.JobId
        elif isinstance(job, STRING):
            job_id = job
        else:
            raise TypeError('''Invalid job type''')
        return job_id

    def create_job(self, job_desc):
        '''
        Create a new job descripted by `job_desc`.

        `job_desc` is a json string, a dict or a Job type instance which
        descripts a new job, you can reference for the job related official
        documentation of BatchCompute service.

        If creation request is accepted by BatchCompute service, it returns a
        response with a string type job id which is a handler you can operate
        later, otherwise, a exception to indicate errors will be raised.

        '''
        job = JobDescription(job_desc)
        # Validate parameters.
        # It will raise an exception if invalid parameters exist.
        job.validate()
        res = self._sa.post('jobs', job.dump())
        return CreateResponse(res, self._h)

    def update_job_priority(self, job, priority):
        '''
        Change the priority of a given job.

        `job_id` is a handler of a job in BatchCompute service, and `priority`
        must be a int vlaue between 0-999.

        Notice:
            Only a stopped job's priority can be changed.

        '''
        job_id = self._get_id(job)
        res = self._sa.put('jobs', job_id,
                           attrs='Priority',
                           body=str(priority))
        return ActionResponse(res, self._h)

    def stop_job(self, job):
        '''
        Stop a running or waiting job specified by `job`.

        Notice:
            Only running or waiting jobs can be stopped.

        '''
        job_id = self._get_id(job)
        p = {'Action': 'Stop'}
        res = self._sa.put('jobs', job_id, params=p)
        return ActionResponse(res, self._h)

    def start_job(self, job):
        '''
        Restart a stopped job specified by `job`.

        Notice:
            Only stopped jobs can be restart.

        '''
        job_id = self._get_id(job)
        p = {'Action': 'Start'}
        res = self._sa.put('jobs', job_id, params=p)
        return ActionResponse(res, self._h)

    def delete_job(self, job):
        '''
        Release a job specified by `job` from BatchCompute sevice.

        Notice:
            Only jobs in stable state(Failed, Stopped, Finished) can be deleted.

        '''
        job_id = self._get_id(job)
        res = self._sa.delete('jobs', job_id)
        return ActionResponse(res, self._h)

    def get_job(self, job):
        '''
        Get a given job's life cycle status information.

        For example:
            clnt = Client(region, id, key)
            job_status = clnt.get_job('job-xxxx')
            print job_status.State
            print job_status.StartTime
            print job_status.NumTotalTask
            ...

        '''
        job_id = self._get_id(job)
        res = self._sa.get('jobs', job_id)
        return GetResponse(res, Job, self._h)

    def get_job_description(self, job):
        '''
        Retrieve a given job's static description from BatchCompute service.

        For example:
            clnt = Client(region, id, key)
            job_desc = clnt.get_job_description('job-xxxx')
            print job_desc.JobName
            print job_desc.TaskDag
            print job_desc.Priority
            ...

        '''
        job_id = self._get_id(job)
        res = self._sa.get('jobs', job_id, 'description')
        return GetResponse(res, JobDescription, self._h)

    def list_jobs(self):
        '''
        Retrive all jobs' life cycle status information from BatchCompute
        service.

        Return a sorted(according to job id) job status list-like object.

        For example:
            clnt = Client(region, id, key)
            job_list = clnt.list_job()
            for job in job_list:
                print job.JobId
                print job.State
                print job.StartTime
                print job.NumTotalTask
            ...

        '''
        res = self._sa.get('jobs')
        return ListResponse(res, Job, self._h)

    def list_tasks(self, job_id):
        '''
        Retrive a job's task and instance status information from BatchCompute
        service.

        Return a sorted(according to start time and task name) task and
        instance status list-like object.

        For example:
            clnt = Client(region, id, key)
            task_list = clnt.list_tasks('job-xxxx')
            for task in task_list:
                print task.TaskName
                print task.State
                for instance in task.InstanceList:
                    print instance.InstanceId
                    print instance.State
            ...

        '''
        res = self._sa.get('jobs', job_id, 'tasks')
        return ListResponse(res, Task, self._h)

    def list_images(self):
        '''
        Retrive all images' information from BatchCompute service.

        Return a sorted(according to image name) list-like object including
        all available images.

        For example:
            clnt = Client(region, id, key)
            image_list = clnt.listImages()
            for image in image_list:
                print image.ImageId
                print image.ImageName
                print image.Description
                print image.Platform
            ...

        '''
        res = self._sa.get('images')
        return ListResponse(res, Image, self._h)

# Add CamelCasedClass metaclass which will change all BatchComputeClient
# user-defined method name to lower-camel-cases. For example: you can invoke
# `listImages` instead of `list_images` method with a BatchComputeClient
# instance.
Client = add_metaclass(Client, CamelCasedClass)
