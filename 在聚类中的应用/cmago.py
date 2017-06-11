#!usr/bin/env python
# encoding: utf-8

'''
通过R产生的数据集对残差函数进行cma优化，g1,g2分别对应y垂直和百分比残差函数
'''
import cma
import fcts
from multiprocessing import Pool
from numpy import *
import pickle
import numpy as np
import time
__author__ = "luzhijun"


def f1(b):
    p = np.array(b) / 100000
    s = b[0] * p[0]
    for x in [1, 2, 3, 4]:
        s += np.sum(b[:(x + 1)]) * np.prod(1 - p[:x]) * p[x]
    s += (np.sum(b[:5]) + 100000) * np.prod(1 - p[:5])
    return s


def dumpData(x, filename):

    with open(filename, 'wb') as f:
        pickle.dump(x, f, pickle.DEFAULT_PROTOCOL)


def cmaUser(func, dim):
    pool = Pool()
    #SM = []
    opts = cma.CMAOptions()
    opts['tolfun'] = 1e-6
    opts['tolfunhist'] = 1e-6
    #opts['tolx'] = 1e-6
    opts['popsize'] = 20
    opts['maxiter'] = 1e5
    opts['bounds'] = [[-2.048] * dim, [2.048] * dim]
    es = cma.CMAEvolutionStrategy(dim * [0], 1, opts)
    while not es.stop():
        #it += 1
        solutions = es.ask()
        es.tell(solutions, pool.map(func, solutions))
        if es.countiter % 20 == 0:
            print(es.countiter, func(solutions[0]))
        # SM.append(es.result()[0])
    # es.logger.add()
    # es.disp()
    # es.result_pretty()
    print(es.result()[1])
    print(es.result()[0])
    print(es.countiter)
    #dumpData(SM, "imqhoa.tl")
    # pylab.figure(1)
    # cma.plot()
    # pylab.show(1)
if __name__ == '__main__':
    s = time.clock()
    cmaUser(fcts.ackley, 500)
    print(time.clock() - s)
