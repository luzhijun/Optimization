#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import cma
import math
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import makeData as md
import time

plt.rc('figure', figsize=(16, 9))
PI=math.pi
E=math.exp
data=md.loadData('data.tl')
X=data[0]
Y=data[1]
RANGE=max(Y)-min(Y)

PN=300
ALPHA=0.01
BETA=PI/18.0

PARTITION=5

DIM=3*PARTITION
SPN=int(PN/PARTITION)
SL=14.0/PARTITION

L=[]
for i in range(PARTITION-1):
    L.append(-7+(i+1)*SL-0.01)



def fittingFunc(param):
	return np.poly1d(param)


def realLineFunc(param):
    def f(x):
        i=int(math.floor((x+7)/SL))
        return np.poly1d(param[3*i:3*(i+1)])(x)
    return f

def mse(x,y,param):
    s=0
    for j in range(0,DIM,3):
        for i in range(int(j/3)*SPN,int(j/3+1)*SPN,1):
            s+=(y[i]-fittingFunc(param[j:j+3])(x[i]))**2
    return math.sqrt(s/PN) 
 #间断点
def evalfunc1(param):
    s=mse(X,Y,param)/RANGE
    a=0
    for j in range(3,DIM,3):
        a+=E(abs(fittingFunc(param[j-3:j])(X[(j/3)*SPN])-fittingFunc(param[j:j+3])(X[(j/3)*SPN]))/RANGE-ALPHA)-1
    return s+a
#间断点一阶导数
def evalfunc2(param):
    s=mse(X,Y,param)/RANGE
    b=0
    for j in range(3,DIM,3):
        b+=(E(abs(math.atan(2*param[j-3]+param[j-2])-math.atan(2*param[j]+param[j+1]))-BETA)-1)/(10*math.e)
    return s+b
#考虑两种
def evalfunc3(param):
    s=mse(X,Y,param)/RANGE
    a=0
    for j in range(3,DIM,3):
        a+=E(abs(fittingFunc(param[j-3:j])(X[(j/3)*SPN])-fittingFunc(param[j:j+3])(X[(j/3)*SPN]))/RANGE-ALPHA)-1
    b=0
    for j in range(3,DIM,3):
        b+=(E((abs(math.atan(2*param[j-3]+param[j-2])-math.atan(2*param[j]+param[j+1]))-BETA))-1)/(10*math.e)
    return s+a+b
#不考虑其他因素
def evalfunc(param):
    s=mse(X,Y,param)/RANGE
    return s


def cmaUser(func):
    pool=Pool()
    t1=time.time()
    es = cma.CMAEvolutionStrategy(DIM * [1], 0.3,{'popsize':15})
    while not es.stop() :
        solutions = es.ask()
        es.tell(solutions,pool.map(func,solutions))
    print 'eval value:%s'%es.result()[1]
    return {'param':es.result()[0],'time':time.time()-t1}

def cmaUser1(func):
    pool=Pool()
    t1=time.time()
    mat=[]
    es = cma.CMAEvolutionStrategy(DIM * [1], 0.3,{'popsize':15})
    while not es.stop() :
        solutions = es.ask()
        es.tell(solutions,pool.map(func,solutions))
        
        mat.append(es.correlation_matrix())
    print 'eval value:%s'%es.result()[1]
    return {'param':es.result()[0],'matrix':mat,'time':time.time()-t1}


def draw1(title):
    global X

    res=cmaUser(evalfunc)
    res1=cmaUser(evalfunc1)
    res2=cmaUser(evalfunc2)
    res3=cmaUser(evalfunc3)

    plt.figure(1) 
    plt.plot(X,Y,'b.',alpha=0.6,label="measure point")
    print L
    X1=np.insert(X,0,L)
    X1.sort()

    plt.plot(X1,map(realLineFunc(res),X1),c="red",lw=2,ls="-",alpha=0.7,label="interval")
    plt.plot(X1,map(realLineFunc(res1),X1),c="blue",lw=2,ls="-",alpha=0.7,label="continuity1")
    plt.plot(X1,map(realLineFunc(res2),X1),c="green",lw=2,ls="-",alpha=0.7,label="continuity2")
    plt.plot(X1,map(realLineFunc(res3),X1),c="black",lw=2,ls="--",alpha=0.7,label="continuity3")
    plt.legend(loc='best')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.show()
    plt.figure(2)
    plt.plot(X,Y,'b.',alpha=0.6,label="measure point")
    plt.plot(X1,map(lambda x:10*math.sin(0.6*x),X1),c="cyan",lw=2,ls="-",alpha=0.7,label="real function")
    plt.plot(X1,map(realLineFunc(res3),X1),c="black",lw=2,ls="--",alpha=0.7,label="continuity3")
    plt.legend(loc='best')
    plt.title("Compare best fitting curve with real curve ")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def draw(title):
    global X

   
    res=cmaUser(evalfunc)
    print L
    X1=np.insert(X,0,L)
    X1.sort()
    plt.figure(2)
    plt.plot(X,Y,'b.',alpha=0.6,label="measure point")
    plt.plot(X1,map(lambda x:10*math.sin(0.6*x),X1),c="cyan",lw=2,ls="-",alpha=0.7,label="real function")
    Y1=map(realLineFunc(res),X1)
    print [X1,Y1]
    plt.plot(X1,Y1,c="black",lw=2,ls="--",alpha=0.7,label="continuity3")
    plt.legend(loc='best')
    plt.title("Compare best fitting curve with real curve ")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def compute():
	S={}
	global PARTITION
	global DIM 
	global SPN
	global SL
	for i in range(5,35,5):
		PARTITION=i
		DIM=3*PARTITION
		SPN=int(PN/PARTITION)
		SL=14.0/PARTITION
		res=cmaUser1(evalfunc)
		res1=cmaUser1(evalfunc1)
		res3=cmaUser1(evalfunc3)
		S[i]=[res,res1,res3]
	md.dumpData(S,'result.tl')
	print 'finished!'

if __name__ == '__main__':
	compute()
    
    















