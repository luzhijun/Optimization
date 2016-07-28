#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import cma,random
import math,pickle
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
        	return  1e7+1e6*math.sin(x)
            #random.seed(x)
            #return  1e10+1000*random.random()
    return funci2(X,a)
    #return 0
    
def cmaUser(mu,sigma,cw=0.1,dim=100,popsize=100):
    restrain=False
    sig=[]
    es = cma.CMAEvolutionStrategy(dim * [mu], sigma,{'popsize':popsize,'bounds':[down, up]})
    while not es.stop() :
        solutions = es.ask()
        es.tell(solutions, [func(p,cw) for p in solutions])
        sig.append(es.sigma)
    if es.result()[1]<0.5e7:
        restrain=True
    return [mu,restrain,sig,es.result()[1],sigma]


result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def main():
    pool=Pool()
    mu=frange(0.05,1,0.2)
    sigma=[1]
    for sig in sigma:
        for m in mu:
            pool.apply_async(cmaUser,(m,sig),callback=log_result)
    pool.close()
    pool.join()
    print 'finshed'
    with open("sigma10.tl",'w') as f:
        pickle.dump(result_list,f,pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':     
    main()











