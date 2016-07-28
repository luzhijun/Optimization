#!usr/bin/env python
#encoding: utf-8
import os
import sys
import config as cfg
from math import sqrt
from simple_oss import SimpleOss
import json

TASK_ID = os.environ.get('ALI_DIKU_TASK_ID')
INSTANCE_COUNT = int(os.environ.get('INSTANCE_COUNT'))
INSTANCE_ID = int(os.environ.get('ALI_DIKU_INSTANCE_ID'))
OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')


oss_clnt = SimpleOss(cfg.OSS_HOST, cfg.ID, cfg.KEY)

def get_json(filePath,instance_count, instance_id):
    json_cfg=oss_clnt.download_str(cfg.BUCKET,cfg.DATA_PATH)
    return json.loads(json_cfg)


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