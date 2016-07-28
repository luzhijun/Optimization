import os
import sys
from math import sqrt

from simple_oss import SimpleOss

INSTANCE_ID = int(os.environ.get('ALI_DIKU_INSTANCE_ID'))
OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')

ID = 'P4c9wtscfsH4rxeT'
KEY = 'i1D0CKk4kVXS0xI1YfN2fJzFVHdW8Y'
BUCKET = 'vp02'

OUTPUT_PATH = 'batch_python_sdk/output/find_task_result_%s.txt'

start_num = 2
end_num = 10000
instance_count = 4
oss_clnt = SimpleOss(OSS_HOST, ID, KEY)

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
    s, e = get_range(start_num, end_num, instance_count, INSTANCE_ID)
    f = open('result.txt', 'w')
    for num in xrange(s, e):
        if is_prime(num):
            f.write(str(num) + '\n')
    f.close()
    oss_clnt.upload(BUCKET, 'result.txt', OUTPUT_PATH%INSTANCE_ID)
    return 0

def main():
    find_task()
    return 0

if __name__ == '__main__':
    sys.exit(main())
