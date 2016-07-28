#!usr/bin/env python
#encoding: utf-8

from time import time
import sys

__author__="luzhijun"


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
if __name__ == '__main__':
        sys.exit(make_file(0.1))







