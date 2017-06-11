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


def qho(k, m, boundary, func, lamb=1, maxcount=100):
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
    boundary = np.array(boundary)
    dim = len(m)
    sigma = boundary[1] - boundary[0] / 2.0
    sigma0 = max(sigma)
    cov = np.diag(sigma**2)
# 高斯分布生成k个中心点，原文是随机生成的，这里初始化不影响
    centers = np.random.multivariate_normal(m, cov, k)
    itercount = 1
    value = pool.map(func, centers)
    xv = np.argsort(value)
    while True:
        #  统计k*lamb个采样点
        ncenters = np.array([[0] * dim])
        for center in centers:
            ncenters = np.vstack((
                ncenters, np.random.multivariate_normal(center, cov, 1)
            ))
        ncenters = ncenters[1:]
        # 简单边界处理
        for i in range(k):
            mark1 = ncenters[i, :] < boundary[0]
            mark2 = ncenters[i, :] > boundary[1]
            ncenters[i, mark1] = boundary[0, mark1]
            ncenters[i, mark2] = boundary[1, mark2]

        nvalue = list(map(func, ncenters))
        xnv = np.argsort(nvalue)
        nsolutions = []
        for i in range(k):
            if value[xv[i]] < nvalue[xnv[i]]:
                nsolutions.append(centers[xv[i]])
            else:
                nsolutions.append(ncenters[xnv[i]])
        nsolutions = np.array(nsolutions)
        # 迭代数递增
        itercount += 1

        #  计算k个中心点的标准差向量
        c = np.std(nsolutions, axis=0)
        # print(min(c))
        if itercount % 2 == 0:
            print('iter', itercount, ': ', func(nsolutions[0]))
        # print(sigma0)
        if abs(max(c - sigma)) < abs(sigma0):
            # update the bad solution
            value = list(map(func, nsolutions))
            itercount += 1
            badIndex = np.argmax(value)
            meanSolution = np.mean(nsolutions, axis=0)
            nsolutions[badIndex] = meanSolution
            c = np.std(nsolutions, axis=0)
            if abs(max(c)) < abs(sigma0):
                sigma0 /= 2.0
                cov = np.diag(np.array([sigma0] * dim)**2)
        else:
            value = nvalue
        if itercount > maxcount:  # sigma0 < critition or
            print('ncenters:%s' % nsolutions[0])
            print('value:%s' % func(nsolutions[0]))
            print('itercount:%d' % itercount)
            return nsolutions[0]
            break
        sigma = c
        centers = nsolutions
        xv = xnv


if __name__ == '__main__':
    try:
        s = time.clock()
        dim = 30
        qho(30, [0] * dim, [[-2.048] * dim, [2.048] * dim],
            fcts.griewank, maxcount=3000)
        print(time.clock() - s)
    except ValueError as err:
        print("OS error: {0}".format(err))
    except TypeError as err:
        print("Type error: {0}".format(err))
