#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
make linear data sets
'''

import numpy as np
import math
import makeData as md
import matplotlib.pyplot as plt
plt.rc('figure', figsize=(16, 9))

dataSet=md.loadData('data.tl')
X=dataSet[0]
Y=dataSet[1]

def realLineFunc(param):
    def f(x):
        i=int(math.floor((x+7)/SL))
        return np.poly1d(param[3*i:3*(i+1)])(x)
    return f


def draw():
    global SL

    data=md.loadData('result.tl')
    for k,v in data.iteritems():
        SL=14.0/k
        L=[]
        for i in range(k-1):
            L.append(-7+(i+1)*SL-0.01)
        X1=np.insert(X,0,L)
        X1.sort()
        plt.figure(k)
        plt.plot(X,Y,'b.',alpha=0.6,label="measure point")
        plt.plot(X1,map(realLineFunc(v[0]['param']),X1),c="red",lw=2,ls="-",alpha=0.7,label="M1")
        plt.plot(X1,map(realLineFunc(v[1]['param']),X1),c="blue",lw=2,ls="-",alpha=0.7,label="M2")
        plt.plot(X1,map(realLineFunc(v[2]['param']),X1),c="black",lw=2,ls="--",alpha=0.7,label="M3")
        plt.plot(X1,map(lambda x:10*math.sin(0.6*x),X1),c="cyan",lw=2,ls="-",alpha=0.7,label="real function")
        plt.legend(loc='best')
        plt.title("fitting interval sin curve with  quadratic curve by %s partition"%k)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('img/img_%s.pdf'%k)

def draw1():
    global SL

    data=md.loadData('result1.tl')
    for k,v in data.iteritems():
        SL=14.0/k
        L=[]
        for i in range(k-1):
            L.append(-7+(i+1)*SL-0.01)
        X1=np.insert(X,0,L)
        X1.sort()
        plt.figure(k)
        plt.plot(X,Y,'b.',alpha=0.6,label="measure point")
        plt.plot(X1,map(realLineFunc(v[0]['param']),X1),c="red",lw=2,ls="-",alpha=0.7,label="M1")
        plt.plot(X1,map(realLineFunc(v[1]['param']),X1),c="blue",lw=2,ls="-",alpha=0.7,label="M2")
        plt.plot(X1,map(realLineFunc(v[3]['param']),X1),c="black",lw=2,ls="--",alpha=0.7,label="M3")
        plt.plot(X1,map(realLineFunc(v[2]['param']),X1),c="green",lw=2,ls="-",alpha=0.7,label="M4")
        plt.plot(X1,map(lambda x:10*math.sin(0.6*x),X1),c="cyan",lw=2,ls="-",alpha=0.7,label="real function")
        plt.legend(loc='best')
        plt.title("fitting interval sin curve with  quadratic curve by %s partition"%k)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('img/img_%s.pdf'%k)



if __name__ == '__main__':   
    draw1()
