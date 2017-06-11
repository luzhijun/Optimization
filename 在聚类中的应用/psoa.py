# encoding: utf-8

import pso
import fcts
import numpy as np
import time

__author__ = "luzhijun"
'''
qho
'''


def f1(b):
    p = np.array(b) / 100000
    s = b[0] * p[0]
    for x in [1, 2, 3, 4]:
        s += np.sum(b[:(x + 1)]) * (1 - np.prod(p[:x])) * p[x]
    s += (np.sum(b[:5]) + 100000) * (1 - np.prod(p[:5]))
    return s


def banana(x):
    x1 = x[0]
    x2 = x[1]
    return x1**4 - 2 * x2 * x1**2 + x2**2 + x1**2 - 2 * x1 + 5


def con(x):
    x1 = x[0]
    x2 = x[1]
    return [-(x1 + 0.25)**2 + 0.75 * x2]

dim = 50
lb = [-10] * dim
ub = [10] * dim


if __name__ == '__main__':
    # a = pso.pso(fcts.griewank, lb, ub, maxiter=1005,
    #             minstep=1e-20, minfunc=1e-20, swarmsize=100, debug=False)
    s = time.clock()
    a = pso.pso(fcts.sphere, [-600] * 30, [600] * 30, maxiter=1000,
                minstep=1e-20, minfunc=1e-20, swarmsize=100, debug=False)
    print(time.clock() - s)
