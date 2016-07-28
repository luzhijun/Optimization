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

def pp(fsize):
	print fsize
	t=time()
	print make_file(fsize)
	print "consume %ss to make_file"%(time()-t)
	
	print "from disk"
	with open("test.iso",'r') as f:
		t=time()
		all=f.read()
		print "consume %ss to read_file"%(time()-t)
		with open("test1.iso",'w') as f1:
			t=time()
			f1.write(all)
			print "consume %ss to write diskfile"%(time()-t)
		with open("/run/shm/test.iso",'w') as f2:
			t=time()
			f2.write(all)
			print "consume %ss to write shmfile"%(time()-t)

	print "from shm"
	with open("/run/shm/test.iso",'r') as f:
		t=time()
		all=f.read()
		print "consume %ss to read_file"%(time()-t)
		with open("/run/shm/test1.iso",'w') as f1:
			t=time()
			f1.write(all)
			print "consume %ss to write shmfile"%(time()-t)
		with open("test2.iso",'w') as f2:
			t=time()
			f2.write(all)
			print "consume %ss to write diskfile"%(time()-t)


	call("(time rm -rf /run/shm/*)",shell=True)
	call("(time rm -rf test*)",shell=True)


def run():
	pp(0.1)
	pp(1)
	pp(2)
	

    
if __name__ == '__main__':
        sys.exit(run())







