#!usr/bin/env python
#encoding: utf-8
import os
import sys
import config as cfg
from math import sqrt
from simple_oss import SimpleOss

TASK_ID = os.environ.get('ALI_DIKU_TASK_ID')
INSTANCE_COUNT = int(os.environ.get('INSTANCE_COUNT'))
INSTANCE_ID = int(os.environ.get('ALI_DIKU_INSTANCE_ID'))
OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')


oss_clnt = SimpleOss(OSS_HOST, cfg.ID, cfg.KEY)

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
    s, e = get_range(cfg.DATA_START, cfg.DATA_END, INSTANCE_COUNT, INSTANCE_ID)
    f = open('result.txt', 'w')
    for num in xrange(s, e):
        if is_prime(num):
            f.write(str(num) + '\n')
    f.close()
    oss_clnt.upload(cfg.OSS_BUCKET, 'result.txt', cfg.FIND_OUTPUT_PATH%INSTANCE_ID)
    return 0

def count_task():
    s = ""
    for instance_id in range(INSTANCE_COUNT):
        instance_result = oss_clnt.download_str(BUCKET, FIND_OUTPUT_PATH%instance_id)
        s+=instance_result
    oss_clnt.upload_str(cfg.OSS_BUCKET, s, cfg.COUNT_OUTPUT_PATH)

def main():
    if TASK_ID == 'Find':
        find_task()
    else:
        count_task()
    return 0

if __name__ == '__main__':
    sys.exit(main())