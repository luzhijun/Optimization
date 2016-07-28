#!usr/bin/env python
#encoding: utf-8
import config as cfg
import os,sys
from time import gmtime, strftime,time
from subprocess import call,PIPE,Popen
from externals.simple_oss import SimpleOss
__author__="luzhijun"


OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')
oss_clnt = SimpleOss(OSS_HOST, cfg.ID, cfg.KEY,cfg.OSS_BUCKET)

def make_file(size):
	size*=1024*1024*1024
	fsize=0
	i=0
	datetime=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

	with open("test.iso",'w') as f:
		while True:
			i+=1
			text=datetime+str(time())+str(fsize+i)
			fsize+=len(text)
			f.write(text)
			if fsize>=size:
				break
	print "finished make_file"
	return fsize

def run():
	t=time()
	print make_file(0.1)
	print "consume %ss to make_file"%(time()-t)
	call("(echo 'read from disk ')>>out",shell=True)
	t=time()
	call("(time cp test.iso /dev/shm/test.iso)2>>out",shell=True)
	print "consume %ss to read from disk"%(time()-t)
	call("(echo 'write in shm ')>>out",shell=True)
	t=time()
	call("(time cp /dev/shm/test.iso /dev/shm/test1.iso)2>>out",shell=True)
	print "consume %ss to write in shm"%(time()-t)
	call("(echo 'read from shm')>>out",shell=True)
	t=time()
	call("(time mv /dev/shm/test1.iso ./)2>>out",shell=True)
	print "consume %ss to read from shm"%(time()-t)
	oss_clnt.upload(cfg.OSS_BUCKET,"out",cfg.RESPONSE_NAME)
    
if __name__ == '__main__':
        sys.exit(run())







