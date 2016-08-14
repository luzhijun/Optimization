#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import cma
import matplotlib.pyplot as plt
import math
import pickle

from multiprocessing import Pool
E=math.exp
D=2

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def dumpData(x,filename):
    with open(filename,'w') as f:
        pickle.dump(x,f,pickle.HIGHEST_PROTOCOL)

def loadData(filename):
    with open(filename,'r') as f:
        x=pickle.load(f)
    return x

def func(X):
    x=X[0]
    y=X[1]
    return 3*(1-x**2)*E(-x**2-(y+1)**2)-10*(x/5.0-x**3-y**5)*E(-x**2-y**2)-E(-(x+1)**2-y**2)/3.0


def cmaUser():
    pool=Pool()
    es = cma.CMAEvolutionStrategy(2 * [3], 0.3,{'popsize':20,'bounds':[-10,10]})
    Xs=[]

    while not es.stop() :
        solutions = es.ask()
        Xs.append(solutions)
        es.tell(solutions,pool.map(func,solutions))
        #es.tell(solutions,[cma.fcts.griewank(s)  for s in solutions])
        es.logger.add()
    es.logger.plot()
    dumpData(Xs,'Xs.tl')
    return es.result_pretty()

if __name__ == '__main__':     
   cmaUser()
   raw_input("Enter any key to quit the pro!")
   exit(0)
    















