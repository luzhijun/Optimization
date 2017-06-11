# encoding: utf-8

import numpy as np
from multiprocessing import Pool
import fcts
import time

critition = 1e-6
__author__ = "luzhijun"
'''
qho
'''


def f1(b):
    p = np.array(b) / 100000
    s = b[0] * p[0]
    for x in [1, 2, 3, 4]:
        s += np.sum(b[:x + 1]) * (1 - np.sum(p[:x])) * p[x]
    s += (np.sum(b[:5]) + 100000) * (1 - np.sum(p[:5]))
    return s


def qho(k, m, boundary, func, lamb=1):
    """mqhoa 迭代过程
    Args:
        k:中心点数
        m:初始均值向量
        boundary:定义域边界
        lamb:初始种群大小
        func:问题函数
    Returns:
    Raise:
        TypeError:类型不准确
        ValueError:值太小

    """

    pool = Pool()
    dim = len(m)
    sigma0 = (boundary[1] - boundary[0]) / 2.0
    sigma = np.array([(boundary[1] - boundary[0]) / 2.0] * dim)
    cov = np.diag(sigma**2)
# 高斯分布生成k个中心点，原文是随机生成的，这里初始化不影响
    centers = np.random.multivariate_normal(m, cov, k)
    itercount = 1
    value = list(pool.map(func, centers))
    while True:
        #  统计k*lamb个采样点
        ncenters = np.array([[0] * dim])
        for center in centers:
            ncenters = np.vstack((
                ncenters, np.random.multivariate_normal(center, cov, 1)
            ))
        # 边界处理
        ncenters = np.where(ncenters[1:] > boundary[1], boundary[1], np.where(
            ncenters[1:] < boundary[0], boundary[0], ncenters[1:]))

        nvalue = list(pool.map(func, ncenters))
        nsolutions = []
        for i in range(k):
            if value[i] < nvalue[i]:
                nsolutions.append(centers[i])
            else:
                nsolutions.append(ncenters[i])
        nsolutions = np.array(nsolutions)

        itercount += 1

        #  计算k个中心点的标准差向量
        c = np.std(nsolutions, axis=0)
        if itercount % 20 == 0:
            print('iter', itercount, ': ', func(nsolutions[0]))
        # print(min(c))
        if abs(max(c - sigma)) < abs(sigma0):
            value = list(pool.map(func, nsolutions))
            itercount += 1
            badIndex = np.argmax(value)
            meanSolution = np.mean(nsolutions, axis=0)
            nsolutions[badIndex] = meanSolution
            c = np.std(nsolutions, axis=0)
            if abs(max(c)) < abs(sigma0):
                sigma = c
                sigma0 /= 2.0
                cov = np.diag(np.array([sigma0] * dim)**2)
            if itercount > 3000:  # sigma0 < critition or
                print('ncenters:%s' % nsolutions[0])
                print('value:%s' % func(nsolutions[0]))
                print('itercount:%d' % itercount)
                break
        else:
            value = nvalue
        sigma = c
        centers = nsolutions


if __name__ == '__main__':
    try:
        s = time.clock()
        qho(30, [0] * 30, [-600, 600], fcts.griewank)
        print(time.clock() - s)
    except ValueError as err:
        print("OS error: {0}".format(err))
    except TypeError as err:
        print("Type error: {0}".format(err))
