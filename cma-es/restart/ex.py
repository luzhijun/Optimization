#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import cma,random
import math
from multiprocessing import Pool
up=1
down=-1

def funci(X,a):
    return sum([a*xi*xi for xi in X])

def funci2(X,a):
	return max([a*abs(xi) for xi in X])

def func(X,cw):
    d=-(up-down)*cw/2.0
    u=(up-down)*cw/2.0
    a=1e7/funci2([u]*len(X),1)
    for x in X:
        if x>u or x<d:
        	return  1e7+1e5*math.sin(x)
            #random.seed(x)
            #return  1e10+1000*random.random()
    return funci2(X,a)
    #return 0

    
def cmaUser(cw,mu=0.3,dim=100,sigma=0.4,popsize=100):
    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize,'bounds':[down, up]})
    while not es.stop() :
        solutions = es.ask()
        es.tell(solutions, [func(p,cw) for p in solutions])
        es.logger.add()
        es.disp()
    es.result_pretty()
    return es.result()

def run(cw,sigma):
    count=1
    res=cmaUser(cw,sigma=sigma)
    while  res[1]>1e6:
        print res
        count+=1
        res=cmaUser(cw,sigma=sigma)
    with open("cw%s_sigma%s_count%s.txt"%(cw,sigma,count),"w+") as f:
            f.write(" ")

def main():
    pool=Pool()
    a=[0.1,0.2,0.3,0.4,0.5]
    cws=[0.1,0.08,0.06,0.04,0.02]
    #a=[0.3]
    #cws=[0.5]
    for cw in cws:
        for sigma in a:
            pool.apply_async(run,(cw,sigma,))
    pool.close()
    pool.join()
    print 'finshed'

if __name__ == '__main__':     
    main()











