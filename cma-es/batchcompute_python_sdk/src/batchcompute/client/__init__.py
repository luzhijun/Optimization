'''
A simple implementation of a client to get BatchCompute Service.

With a `Client` instance, you can create new jobs, list all running jobs,
get a job status, stop a running job, restart a stopped job, or list all
available images, and so on.
'''


__all__ = [
    "Client",
]

from .client import Client
