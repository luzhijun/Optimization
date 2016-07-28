import time
import sys
import unittest

from batchcompute import (
    JobDescription, TaskDescription, TaskDag, ResourceDescription, Client,
    ClientError, CN_QINGDAO
)

class ClientE2ETest(unittest.TestCase):
    def setUp(self):
        self.endpoint = CN_QINGDAO
        self.access_key_id = ""
        self.access_key_secret = ""
        self.image_id = ''

        self.client = Client(self.endpoint, self.access_key_id,
                        self.access_key_secret, human_readable=True)
        self.job_id = None

    def _get_job_desc(self):
        job_desc = JobDescription()
        find_task = TaskDescription()
        res_desc = ResourceDescription()

        find_task.PackageUri = "oss://your-bucket/batch_python_sdk/worker.tar.gz"
        find_task.ProgramName = 'find_prime_worker.py'
        find_task.ProgramType = 'python'
        find_task.ImageId = self.image_id
        find_task.InstanceCount = 3
        find_task.EnvironmentVariables = {}
        find_task.StdoutRedirectPath = "oss://your-bucket/batch_python_sdk/logs/"
        find_task.StderrRedirectPath = "oss://your-bucket/batch_python_sdk/logs/"
        find_task.ResourceDescription = res_desc

        # Create count task. 
        count_task = TaskDescription(find_task)
        count_task['InstanceCount'] = 1

        # Create task dag.
        task_dag = TaskDag()
        task_dag.add_task(task_name='Find', task=find_task)
        task_dag.add_task(task_name='Count', task=count_task)
        task_dag.Dependencies = {
            'Find': ['Count']
        }

        # count prime job description.
        job_desc.TaskDag = task_dag
        job_desc.JobName = 'PythonSDK'
        job_desc.Priority = 0
        return job_desc

    def tearDown(self):
        while True:
            if self.job_id and self.job_id in self.client.list_jobs():
                state = self.client.get_job(self.job_id).State
                if state in ['Waiting', 'Running']:
                    self.client.stop_job(self.job_id)
                else:
                    self.client.delete_job(self.job_id)
            else:
                break
        self.job_id = None


    def test_create_job(self):
        job_desc = self._get_job_desc()

        # Create jobs.
        job = self.client.create_job(job_desc)
        self.job_id = job.JobId

        self.assertTrue(self.job_id)

    def test_stop_job(self):
        job_desc = self._get_job_desc()

        job = self.client.create_job(job_desc)
        self.job_id = job.JobId
        state = self.client.get_job(job).State
        if state in ['Waiting', 'Running']:
            self.client.stop_job(job)
        self.assertRaises(ClientError, self.client.stop_job, job)

    def test_update_priority(self):
        old_priority = 100
        new_priority = 200

        job_desc = self._get_job_desc()
        job_desc.Priority = old_priority

        # Create jobs.
        job = self.client.create_job(job_desc)
        self.job_id = job.JobId
        status = self.client.get_job(job)
        self.assertEqual(status.Priority, old_priority)

        # update priority.
        self.assertRaises(ClientError, self.client.update_job_priority, job, new_priority)
        try:
            self.client.update_job_priority(job, new_priority)
        except ClientError as e:
            code = e.get_code()
            msg = e.get_msg()
            request_id = e.get_requestid()
        else:
            self.assertFalse(False, 'ClientError should be raised')
        status = self.client.get_job(job)
        if status.State in ['Waiting', 'Running']:
            self.client.stop_job(job)
        self.client.update_job_priority(job, new_priority)
        status = self.client.get_job(job)
        self.assertEqual(status.Priority, new_priority)

    def test_start_job(self):
        job_desc = self._get_job_desc()
        job = self.client.create_job(job_desc)
        self.job_id = job.JobId

        self.assertRaises(ClientError, self.client.start_job, job)
        status = self.client.get_job(job)
        if status.State in ['Waiting', 'Running']:
            self.client.stop_job(job)

    def test_list_images(self):
        image_list = self.client.list_images()
        for img in image_list:
            self.assertTrue(hasattr(img, 'ImageId'))
            self.assertTrue(not hasattr(img, 'ResourceId'))
            print(img.ImageId)

    def test_list_tasks(self):
        job_desc = self._get_job_desc()
        job = self.client.create_job(job_desc)
        self.job_id = job.JobId

        task_list = self.client.list_tasks(self.job_id)
        for task in task_list:
            print(task.TaskName)
            for instance in task.InstanceList:
                print(instance.InstanceId)


if __name__ == '__main__':
    unittest.main()
