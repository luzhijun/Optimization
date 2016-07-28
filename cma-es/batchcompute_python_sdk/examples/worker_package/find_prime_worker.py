import os
import sys
from math import sqrt

from simple_oss import SimpleOss

#OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')
OSS_HOST="oss-cn-shenzhen.aliyuncs.com"

ID = 'P4c9wtscfsH4rxeT'
KEY = 'i1D0CKk4kVXS0xI1YfN2fJzFVHdW8Y'
BUCKET = 'vp02'

OUTPUT_PATH = 'batch-python-sdk/output/find_task_result.txt'

start_num = 2
end_num = 10000
oss_clnt = SimpleOss(OSS_HOST, ID, KEY)

def find_task():
    is_prime = lambda x: 0 not in [ x%d for d in range(2, int(sqrt(x))+1)]
    f = open('result.txt', 'w')
    for num in xrange(start_num, end_num):
        if is_prime(num): 
            f.write(str(num) + '\n') 
    f.close()
    oss_clnt.upload(BUCKET, 'result.txt', OUTPUT_PATH)
    return 0

def main():
    find_task()
    return 0

if __name__ == '__main__':
    sys.exit(main())
