#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import cma
import time
import numpy as np
import matplotlib.pyplot as plt
import pickle

from multiprocessing import Pool
up=2
down=-2


def testFunc(X):
    #time.sleep(0.1)
    return cma.fcts.rosen(X)

rec=lambda v,p:map(lambda x:x/float(p),v)
#归一化
def autoNormal(X):
    maxV=map(max,X)
    nV=[X[i]/maxV[i]  for i in range(len(maxV))]
    return nV


def makeCluster(X,threshold):
 
    X=autoNormal(X)
    l=len(X)
    i=0
    remove=set()
    clu=[]
    for xi in range(l):
        clu.append([xi])
    while i<l:
        if i in remove:
            i+=1
            continue
        for j in range(i+1,l):
            M=sum((X[i]-X[j])**2)
            if M<threshold and j not in remove:
                remove.add(j)
                clu[i].append(j)
        i+=1
    for xi in remove:
        clu.remove([xi])
    return clu

def makeEvals(solutions,threshold):
    '''
    make Function values use makeCluster.
    '''
    clu=makeCluster(solutions,threshold)
    evalKeys=[x[0] for x in clu]
    evalValues=map(testFunc,[solutions[ei] for ei in evalKeys])
    evals=[]

    for i,ci in enumerate(clu):
        for j in range(len(ci)):
            evals.append(evalValues[i])
    return  evals

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)


    
def cmaUser(mu=0.5,dim=100,sigma=0.3,popsize=120):
    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize,'bounds':[down, up]})
    sigmas=[]
    t1=time.time()
    while not es.stop() :
        solutions = es.ask()
        sigmas.append(es.sigma)
        values=map(testFunc,solutions)
        es.tell(solutions,values)
    return sigmas,es.countiter,es.result()[1],es.result()[0],time.time()-t1,"normal"

def cmaUser1(dis,mu=0.5,dim=100,sigma=0.3,popsize=120):
    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize,'bounds':[down, up]})
    sigmas=[]
    t1=time.time()
    while not es.stop() :
        solutions = es.ask()
        sigmas.append(es.sigma)
        if es.sigma<sigma*0.1:
            values=makeEvals(solutions,dis)
        else:
            values=map(testFunc,solutions)
        es.tell(solutions,values)
    return sigmas,es.countiter,es.result()[1],es.result()[0],time.time()-t1,"cluster distance:%s"%dis



def main():
    dis=[1e-4,1e-5,1e-6]
    pool=Pool()
    for disi in dis:
        pool.apply_async(cmaUser1,args=(disi,),callback = log_result)
    pool.apply_async(cmaUser,callback = log_result)
    pool.close()
    pool.join()
    print "finished"
    plt.figure(1)
    plts=[]
    length=len(result_list)
    for i in range(length):
        p1,=plt.plot(result_list[i][0])
        plts.append(p1)
        print('iter count:%s'%result_list[i][1])
        print result_list[i][2]
        print result_list[i][3]
        print result_list[i][4]
        print result_list[i][5]
        print "------------"
    plt.plot([0.015]*8000,'--')   
    plt.ylabel('s    plt.ylim(0,0.1)igma')
    plt.xlabel('counter')
    plt.title('dim=100,popsize=150')
    plt.legend(plts,[result_list[i][5] for i in range(length)])
    plt.savefig(u'fig.pdf')

def main1():
    dis=[1e-3,1e-4,1e-5,1e-6]
    pool=Pool()
    for disi in dis:
        pool.apply_async(cmaUser1,args=(disi,),callback = log_result)
    pool.apply_async(cmaUser,callback = log_result)
    pool.close()
    pool.join()
    print "finished"
    with open('data.tl','w') as f:
        pickle.dump(result_list,f,pickle.HIGHEST_PROTOCOL)


def testtime(dis,mu=0.5,dim=100,sigma=0.3,popsize=120):
    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize,'bounds':[down, up]})
    t1=time.time()
    i=0
    while i<3:
        solutions = es.ask()
        values=makeEvals(solutions,dis)
        #values=map(testFunc,solutions)
        es.tell(solutions,values)
        i+=1
    print (time.time()-t1)/3.0*100

if __name__ == '__main__':     
    #print cmaUser1(0.0001)
    #main1()
    #testtime(0.01)
    testtime(0.001)















