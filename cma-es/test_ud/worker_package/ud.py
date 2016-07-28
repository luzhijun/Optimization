#!usr/bin/env python
#encoding: utf-8
import config as cfg
import os,sys,time
from optparse import OptionParser
from externals.simple_oss import SimpleOss
from multiprocessing import Pool
__author__="luzhijun"

TASK_ID = os.environ.get('ALI_DIKU_TASK_ID')
#INSTANCE_COUNT = int(os.environ.get('INSTANCE_COUNT'))
INSTANCE_ID = int(os.environ.get('ALI_DIKU_INSTANCE_ID'))
OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')
oss_clnt = SimpleOss(OSS_HOST, cfg.ID, cfg.KEY,cfg.OSS_BUCKET)
str_list=[]
t=[]
rec='%s %s\n'
def opt_parser(args):
    parser = OptionParser()
    parser.add_option('-m', '--start',
                      action='store', type='int', dest='m')
    parser.add_option('-s', '--end',
                      action='store', type='int', dest='sync')
    (options, args) = parser.parse_args(args)
    return options

def download(num):
    t1=time.time()
    oss_clnt.download_str(cfg.OSS_BUCKET,cfg.REQUEST_NAME)
    return rec%(num,time.time()-t1)

def response(num):
    t1=time.time()
    oss_clnt.upload_str(cfg.OSS_BUCKET,'test',cfg.TMPFILE)
    return rec%(num,time.time()-t1)

def run():
    opts = opt_parser(sys.argv[1:])
    m=int(opts.m)
    sync=int(opts.sync)
    pool=Pool(processes=cfg.CPU_NUM)
    if  TASK_ID == 'download':
        func=download
    elif TASK_ID == 'upload':
        func=response
    else:
        raise AttributeError("没有要处理的task")
    if m<=0:
        raise ValueError("m必须大于0")
        return 1
    t=time.time()
    #同步处理
    if sync is not 0:
        for i in range(m):
            res=pool.apply_async(func,(i,))
            str_list.append(res.get(timeout=10))
    #顺序处理
    else:
        for i in range(m):
            str_list.append(func(i))
    str_list.append(rec%(m,time.time()-t))
    pool.close()
    pool.join()
    context=''.join(str_list)
    oss_clnt.upload_str(cfg.OSS_BUCKET,context,cfg.OUTPUTLOG%INSTANCE_ID)

if __name__ == '__main__':
        sys.exit(run())







