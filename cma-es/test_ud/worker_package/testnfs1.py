#!usr/bin/env python
#encoding: utf-8
import config as cfg
import os,sys
from multiprocessing import Pool
from time import time
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
	path=os.path.join(cfg.LOCAL_DATA,"tmp.txt")
	if os.path.exists(path):
		f = open(path)
		print f.readline()
		f.close()
	return rec%(num,time()-t1)

def run():

	m=cfg.M
	pool=Pool(processes=cfg.CPU_NUM)
	for i in range(m):
		res=pool.apply_async(nfs_read,(i,))
		str_list.append(res.get(timeout=10))
	pool.close()
	str_list.append('-----------')
	print '--------------------'
	pool.join()
	for i in range(m):
		str_list.append(nfs_read(i))
	context=''.join(str_list)
	print context


    
if __name__ == '__main__':
        sys.exit(run())







