#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import cma
import time
import matplotlib.pyplot as plt
import pickle
import math

from multiprocessing import Pool



result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

    
def cmaUser(dim,popsize,mu=0.5,sigma=0.3):
    a=0
    b=0
    c=0
    d=0
    sigma_str=[]

    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize})
    t1=time.time()
    while not es.stop() :
        solutions = es.ask()
        sigma_str.append(es.sigma)
        values=map(cma.fcts.sphere,solutions)
        es.tell(solutions,values)
    a+=es.countiter
    b+=es.countevals
    c+=es.result()[1]
    d+=time.time()-t1
    return a,b,c,d,popsize,'sphere',sigma_str


def cmaUser1(dim,popsize,mu=0.5,sigma=0.3):

    a=0
    b=0
    c=0
    d=0
    sigma_str=[]
    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize})
    t1=time.time()
    while not es.stop() :
        solutions = es.ask()
        sigma_str.append(es.sigma)
        values=map(cma.fcts.cigar,solutions)
        es.tell(solutions,values)
    a+=es.countiter
    b+=es.countevals
    c+=es.result()[1]
    d+=time.time()-t1
    return a,b,c,d,popsize,'cigar',sigma_str


def cmaUser2(dim,popsize,mu=0.5,sigma=0.3):

    a=0
    b=0
    c=0
    d=0
    sigma_str=[]
    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize})
    t1=time.time()
    while not es.stop() :
        solutions = es.ask()
        sigma_str.append(es.sigma)
        values=map(cma.fcts.elli,solutions)
        es.tell(solutions,values)
    a+=es.countiter
    b+=es.countevals
    c+=es.result()[1]
    d+=time.time()-t1
    return a,b,c,d,popsize,'elli',sigma_str

def fig():
    with open("data.tl",'r') as f:
        result_list=pickle.load(f)
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
        print ''.join(['---']*20)
    plt.plot([0.003]*8000,'--')
    plt.ylim(0,0.003)
    plt.xlim(6000,8000)
    plt.ylabel('sigma')
    plt.xlabel('counter')
    plt.title('dim=100,popsize=120')
    plt.legend(plts,[result_list[i][5] for i in range(length)],loc=0,fontsize=10,framealpha=0.5)
    #plt.show()
    plt.savefig("1a.pdf")

def main():
    dim=100
    pool=Pool()
    pops=[5,10,14,18,20,22,26,60,100,140,180,220]
    for pi in pops:
        pool.apply_async(cmaUser,args=(dim,pi,),callback = log_result)
        pool.apply_async(cmaUser1,args=(dim,pi,),callback = log_result)
        pool.apply_async(cmaUser2,args=(dim,pi,),callback = log_result)
    pool.close()
    pool.join()
    print "finished"
    with open('0.5','w') as f:
        pickle.dump(result_list,f,pickle.HIGHEST_PROTOCOL)
if __name__ == '__main__':     
    #print cmaUser1(0.0001)
    #main1()
    #testtime(0.01)
    main()
    















