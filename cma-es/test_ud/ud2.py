#!usr/bin/env python
#encoding: utf-8
import config as cfg
import os,sys,time
from optparse import OptionParser
from externals.simple_oss import SimpleOss
from multiprocessing import Pool
__author__="luzhijun"


oss_clnt = SimpleOss(cfg.OSS_HOST, cfg.ID, cfg.KEY,cfg.OSS_BUCKET)
str_list=[]
filen='test/big'
rec='%s %s\n'
def opt_parser(args):
    parser = OptionParser()
    parser.add_option('-m', '--start',
                      action='store', type='int', dest='m')
    parser.add_option('-s', '--end',
                      action='store', type='int', dest='sync')
    (options, args) = parser.parse_args(args)
    return options

def download1(OSS_BUCKET,filen1):
    while not oss_clnt.exists(cfg.OSS_BUCKET,filen1):
        time.sleep(0.1)
    oss_clnt.download(OSS_BUCKET,'a',filen1)
    return time.time()

def download2(OSS_BUCKET,filen1):
    oss_clnt.download(cfg.OSS_BUCKET,'b',filen1)
    return time.time()
def upload(a,b,c):
    oss_clnt.upload(a,b,c)
    return time.time()

def response(num):
    t1=time.time()
    oss_clnt.upload_str(cfg.OSS_BUCKET,'test',cfg.TMPFILE)
    return rec%(num,time.time()-t1)

def run():
    pool=Pool()
    t2=time.time()
    r2=pool.apply_async(download2,(cfg.OSS_BUCKET,filen,))
    str_list.append(rec%('start_download',t2))
    t3=time.time()
    r3=pool.apply_async(upload,(cfg.OSS_BUCKET,'oss_sdk.pdf',filen,))
    str_list.append(rec%('start_upload',t3))

    t22=r2.get()
    t33=r3.get()
    str_list.append(rec%('finish_download',t33))
    str_list.append(rec%('finish_upload',t22))
    print ''.join(str_list)

if __name__ == '__main__':
        sys.exit(run())







