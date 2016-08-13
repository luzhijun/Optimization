#!usr/bin/env python
#encoding: utf-8
import config as cfg
import os,sys
from multiprocessing import Pool
from time import time,clock
from subprocess import call,PIPE,Popen
from externals.simple_oss import SimpleOss
__author__="luzhijun"


OSS_HOST = os.environ.get('ALI_DIKU_OSS_HOST')
oss_clnt = SimpleOss(OSS_HOST, cfg.ID, cfg.KEY,cfg.OSS_BUCKET)
str_list=[]
rec='%s %s\n'

def make_file1(size):
	p=size*1024*1024*1024-1
	with open("test.iso",'w') as f:
		f.seek(p)
		f.writelines('end')
		f.write('\x00')

def make_file(size):
	size*=1024*1024*1024
	fsize=0
	i=0
	datetime="strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime())"
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

def nfs_read(num):
	t1=time()
	path=os.path.join(cfg.LOCAL_DATA,"ymp.txt")
	if os.path.exists(path):
		f = open(path,'r')
		f.readline()
		f.close()
	return rec%(num,time()-t1)

def nfs_write(num):
	t1=time()
	oss_clnt.upload_str(cfg.OSS_BUCKET,"asdas","test/data/ymp.txt")
	return rec%(num,time()-t1)
def run():
	'''
	t=time()
	print make_file(1)
	print "consume %ss to make_file"%(time()-t)
	call("(ls -al  /run/shm)>>out",shell=True)
	call("(df -h --total)>>out",shell=True)

	

	call("(echo 'read from disk ')>>out",shell=True)
	t=time()
	call("(time cp test.iso /run/shm/test.iso)2>>out",shell=True)
	print "consume %ss to read from disk"%(time()-t)
	call("(echo 'write in shm ')>>out",shell=True)
	t=time()
	call("(time cp /run/shm/test.iso /run/shm/test1.iso)2>>out",shell=True)
	print "consume %ss to write in shm"%(time()-t)
	call("(echo 'read from shm')>>out",shell=True)
	t=time()
	call("(time mv /run/shm/test1.iso ./)2>>out",shell=True)
	print "consume %ss to read from shm"%(time()-t)
	oss_clnt.upload(cfg.OSS_BUCKET,"out",cfg.RESPONSE_NAME)


	
	print "read from nfs "
	t=time()
	c=clock()
	path = os.path.join(cfg.LOCAL_DATA, "test.iso")
	if os.path.exists(path):
		f = open(path,'r')
		f.read()
		f.close()
	print "consume %ss to read from nfs,cpu time:%s"%(time()-t,clock()-c)

	print "read from oss"
	t=time()
	c=clock()
	oss_clnt.download(cfg.OSS_BUCKET,"tmp.iso","test/data/test.iso")
	print "consume %ss to read from oss,cpu time:%s"%(time()-t,clock()-c)
	'''

	m=cfg.M
	pool=Pool(processes=cfg.CPU_NUM)
	for i in range(m):
		res1=pool.apply_async(nfs_read,(i,))
		str_list.append(res1.get(timeout=10))
	pool.apply_async(nfs_write,(1,))
	pool.close()
	pool.join()
	str_list.append('-----------')
	print '--------------------'
	'''
	for i in range(m):
		str_list.append(nfs_read(i))
	'''
	pool=Pool(processes=cfg.CPU_NUM)
	for i in range(m):
		res1=pool.apply_async(nfs_read,(i,))
		str_list.append(res1.get(timeout=10))
	pool.close()
	pool.join()

	context=''.join(str_list)
	print context

	path=os.path.join(cfg.LOCAL_DATA,"ymp.txt")
	if os.path.exists(path):
		f = open(path)
		print f.readline()
		f.close()
	

    
if __name__ == '__main__':
        sys.exit(run())







