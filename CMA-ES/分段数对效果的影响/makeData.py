#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
make linear data sets
'''

import pickle
import numpy as np
import random as rd
import math
PN=300

def dumpData(x,filename):
    with open(filename,'w') as f:
        pickle.dump(x,f,pickle.HIGHEST_PROTOCOL)

def loadData(filename):
    with open(filename,'r') as f:
        x=pickle.load(f)
    return x

def linefunc2(x):
    return 10*math.sin(0.6*x)+rd.uniform(-1.5,1.5)*rd.gauss(0,5)


if __name__ == '__main__':   
	X=np.linspace(-7,7,PN+1)
	X=np.delete(X,len(X)-1,0)
	Y=map(linefunc2,X)
	dumpData([X,Y],'data1.tl')