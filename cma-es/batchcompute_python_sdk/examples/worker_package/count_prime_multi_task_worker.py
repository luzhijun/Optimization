import os
import sys
from math import sqrt

from simple_oss import SimpleOss

INSTANCE_ID = int(os.environ.get('ALI_DIKU_INSTANCE_ID'))
TASK_ID = os.environ.get('ALI_DIKU_TASK_ID')
INSTANCE_COUNT = int(os.environ.get('INSTANCE_COUNT'))
OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')

ID = 'P4c9wtscfsH4rxeT'
KEY = 'i1D0CKk4kVXS0xI1YfN2fJzFVHdW8Y'
BUCKET = 'vp02'

FIND_OUTPUT_PATH = 'batch-python-sdk/output/find_task_result_%s.txt'
COUNT_OUTPUT_PATH = 'batch-python-sdk/output/count_task_result.txt'

start_num = 2
end_num = 10000
instance_count = 2
oss_clnt = SimpleOss(OSS_HOST, ID, KEY)
print os.environ

def get_range(start, end, instance_count, instance_id):
    '''
    A function to split all numbers into 'instance_count' part totally
    and return the start and end number of the 'instance_id' part.
    '''
    total = end - start
    step = total / instance_count
    assert step, 'total numbers should be bigger than instance_count.'
    residue = total % instance_count
    l = [step+1 if i<residue else step for i in range(instance_count)]
    s = sum(l[:instance_id])
    e = s + l[instance_id]
    return s, e

def find_task():
    is_prime = lambda x: 0 not in [ x%d for d in range(2, int(sqrt(x))+1)]
    s, e = get_range(start_num, end_num, INSTANCE_COUNT, INSTANCE_ID)
    f = open('result.txt', 'w')
    for num in xrange(s, e):
        if is_prime(num):
            f.write(str(num) + '\n')
    f.close()
    oss_clnt.upload(BUCKET, 'result.txt', FIND_OUTPUT_PATH%INSTANCE_ID)
    return 0

def count_task():
    prime_list = []
    for instance_id in range(INSTANCE_COUNT):
        instance_result = oss_clnt.download_str(BUCKET, FIND_OUTPUT_PATH%instance_id)
        prime_list += instance_result.splitlines()
    count = len(prime_list)
    oss_clnt.upload_str(BUCKET, str(count), COUNT_OUTPUT_PATH)

def main():
    if TASK_ID == 'Find':
        find_task()
    else:
        count_task()
    return 0

if __name__ == '__main__':
    sys.exit(main())
