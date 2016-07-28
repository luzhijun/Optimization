import os
import sys
import base64
from optparse import OptionParser
from math import sqrt

from simple_oss import SimpleOss

TASK_ID = os.environ.get('ALI_DIKU_TASK_ID')
INSTANCE_ID = int(os.environ.get('ALI_DIKU_INSTANCE_ID'))
OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')

ID = 'P4c9wtscfsH4rxeT'
KEY = 'i1D0CKk4kVXS0xI1YfN2fJzFVHdW8Y'

oss_clnt = SimpleOss(OSS_HOST, ID, KEY)

def opt_parser(args):
    parser = OptionParser()
    parser.add_option('-s', '--start',
                      action='store', type='int', dest='start')
    parser.add_option('-e', '--end',
                      action='store', type='int', dest='end')
    parser.add_option('-d', '--dpath',
                      action='store', type='string', dest='data_path')
    parser.add_option('-o', '--opath',
                      action='store', type='string', dest='output_path')
    parser.add_option('-b', '--bucket',
                      action='store', type='string', dest='bucket')
    parser.add_option('-c', '--inscount',
                      action='store', type='int', dest='ins_count')
    parser.add_option('-l', '--lpath',
                      action='store', type='string', dest='lpath')
    (options, args) = parser.parse_args(args)
    return options

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

def find_task(options):
    is_prime = lambda x: 0 not in [ x%d for d in range(2, int(sqrt(x))+1)]
    count = 0
    s, e = get_range(options.start, options.end, options.ins_count, INSTANCE_ID)
    f = open('result.txt', 'w')
    for num in xrange(s, e):
        if is_prime(num): f.write(str(num) + '\n')
    f.close()
    oss_path = os.path.join(options.data_path, 'count-instance-%s'%(INSTANCE_ID, ))
    oss_clnt.upload(options.bucket, 'result.txt', oss_path)
    return 0

def count_task(options):
    sum = 0
    for i in range(options.ins_count):
        file = 'count-instance-%s'%(i, )
        path = os.path.join(options.local_path, file)
        if os.path.exists(path):
            f = open(path)
            sum += len(f.read().splitlines())
            f.close()
    oss_clnt.upload_str(options.bucket, str(sum), options.output_path)
    return 0

def main():
    opts = opt_parser(sys.argv[1:])
    if TASK_ID == 'Find':
        find_task(opts)
    else:
        count_task(opts)
    return 0

if __name__ == '__main__':
    sys.exit(main())
