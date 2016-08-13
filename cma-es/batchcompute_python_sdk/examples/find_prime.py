import os
import sys
import copy
import time
import tarfile
import base64
sys.path.append('../../')

from externals.simple_oss import SimpleOss
from batchcompute import (
    Client, JobDescription, TaskDag, TaskDescription, ResourceDescription,
)
import config as cfg


def upload_worker(bucket, local_dir, oss_path):
    '''
    A function to help upload worker package to oss.
    '''
    oss_clnt = SimpleOss(cfg.OSS_HOST, cfg.ID, cfg.KEY)
    local_tarfile = 'worker.tar.gz'
    if os.path.exists(local_tarfile): os.remove(local_tarfile)

    def do_tar(worker_dir, tar_file):
        '''
        A function to tar worker package.
        '''
        tar = tarfile.open(tar_file, 'w:gz')
        cwd = os.getcwd()
        os.chdir(worker_dir)
        for root,dir,files in os.walk('.'):
            for file in files:
                tar.add(os.path.join(root, file))
        os.chdir(cwd)
        tar.close()

    do_tar(local_dir, local_tarfile)
    oss_clnt.upload(bucket, local_tarfile, oss_path)

def get_job_desc(package_path, verbose=True):
    job_desc = JobDescription()
    find_task = TaskDescription()

    # Create find task.
    find_task.PackageUri = package_path
    find_task.ProgramArguments = ''
    find_task.ProgramName = 'find_prime_worker.py'
    find_task.ProgramType = 'python'
    find_task.ImageId = cfg.IMAGE_ID
    find_task.InstanceCount = 1
    find_task.EnvironmentVariables = {}
    find_task.StdoutRedirectPath = cfg.LOG_PATH
    find_task.StderrRedirectPath = cfg.LOG_PATH

    # Create task dag.
    task_dag = TaskDag()
    task_dag.add_task(task_name='Find', task=find_task)

    # find prime job description.
    job_desc.TaskDag = task_dag
    job_desc.JobName = 'find-prime'
    job_desc.Priority = 1
    return job_desc

def main():
    upload_worker(cfg.OSS_BUCKET, 'worker_package', cfg.PACKAGE_PATH)

    # Submit job to batch compute.
    clnt = Client(cfg.REGION, cfg.ID, cfg.KEY)
    job_json = get_job_desc(cfg.FULL_PACKAGE)
    job = clnt.create_job(job_json)

    t = 10
    print('Sleep %s second, please wait.'%t)
    time.sleep(t)

    # Wait for jobs terminated.
    while(True):
        s = clnt.get_job(job)
        if s.State in ['Waiting', 'Running']:
            print('Job %s is now %s'%(job, s.State))
            time.sleep(3)
            continue
        else:
            # 'Failed', 'Stopped', 'Finished'
            print('Job %s is now %s'%(job, s.State))
            if s.State == 'Finished':
                oss_clnt = SimpleOss(cfg.OSS_HOST, cfg.ID, cfg.KEY)
                result = oss_clnt.download_str(cfg.OSS_BUCKET, cfg.OUTPUT_PATH)
                # Print out all prime numbers from 0 to 10000.
                print result.splitlines()
            break
    clnt.delete_job(job)

if __name__ == '__main__':
    main()
