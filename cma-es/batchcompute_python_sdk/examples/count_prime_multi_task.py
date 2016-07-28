import os
import time
import tarfile

from externals.simple_oss import SimpleOss
from batchcompute import (
    Client, JobDescription, TaskDag, TaskDescription, ResourceDescription
)
import config as cfg


oss_clnt = SimpleOss(cfg.OSS_HOST, cfg.ID, cfg.KEY)
def upload_worker(bucket, local_dir, oss_path):
    '''
    A function to help upload worker package to oss.
    '''
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
    find_task.ProgramName = 'find_prime_multi_instance_worker.py'
    find_task.ProgramType = 'python'
    find_task.ImageId = cfg.IMAGE_ID
    #find_task.InstanceCount = cfg.COUNT_TASK_NUM
    find_task.InstanceCount = 3
    find_task.EnvironmentVariables = {}
    find_task.StdoutRedirectPath = cfg.LOG_PATH
    find_task.StderrRedirectPath = cfg.LOG_PATH

    # Create count task. 
    count_task = TaskDescription(find_task)
    count_task.InstanceCount = 1

    # Create task dag.
    task_dag = TaskDag()
    task_dag.add_task(task_name='Find', task=find_task)
    task_dag.add_task(task_name='Count', task=count_task)
    task_dag.Dependencies = {
        'Find': ['Count']
    }

    # count prime job description.
    job_desc.TaskDag = task_dag
    job_desc.JobName = 'PythonSDK2'
    job_desc.Priority = 1
    return job_desc

def main():
    upload_worker(cfg.OSS_BUCKET, 'worker_package', cfg.PACKAGE_PATH)

    # Submit job to batch compute.
    clnt = Client(cfg.REGION, cfg.ID, cfg.KEY)
    job_json = get_job_desc(cfg.FULL_PACKAGE)
    job = clnt.create_job(job_json)

    t = 5
    print 'Sleep %s second, please wait.'%t
    time.sleep(t)

    # Wait for job terminated.
    while(True):
        s = clnt.get_job(job)
        if s.State in ['Waiting']:
            print('Job %s is now %s'%(job, s.State))
            time.sleep(10)
            t+=1
            continue
        elif s.State in['Running']:
            print "Waiting%s s"%t
            t=0
            print('Job %s is now %s'%(job, s.State))
            time.sleep(10)
            t+=1
        else:
            # 'Failed', 'Stopped', 'Finished'
            print('Job %s is now %s'%(job, s.State))
            print "running%s s"%t
            if s.State == 'Finished':
                # Print out total prime numbers from 0 to 10000.
                result = oss_clnt.download_str(cfg.OSS_BUCKET, cfg.COUNT_OUTPUT_PATH)
                print('Total %s prime numbers from %s to %s.'%(result, 1, 10000))
            break
    clnt.delete_job(job)

if __name__ == '__main__':
    main()
