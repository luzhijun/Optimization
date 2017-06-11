# encoding: utf-8

import numpy as np
import sys
from multiprocessing import Pool
import fcts

critition = 1e-6
__author__ = "luzhijun"
'''
qho
'''


def qho(k, m, boundary,  func,lamb=1):
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
    sigma0=(boundary[1] - boundary[0])/2.0
    sigma = np.array([(boundary[1] - boundary[0]) / 2.0]*dim)
    cov = np.diag(sigma**2)
# 高斯分布生成k个中心点，原文是随机生成的，这里初始化不影响
    centers = np.random.multivariate_normal(m, cov, k)
    itercount = 1

    while True:
        #  统计k*lamb个采样点
        solutions = np.array([[0]*dim])
        for center in centers:
            solutions = np.vstack((
                solutions, np.random.multivariate_normal(center, cov, 1)
            ))
        solutions=solutions[1:]
        value=list(pool.map(func, centers))
        nvalue = list(pool.map(func, solutions))
        nsolutions=[]
        for i in range(k):
            if value[i]<nvalue[i]:
                nsolutions.append(centers[i])
            else:
                nsolutions.append(solutions[i])
        nsolutions=np.array(nsolutions)
        # 边界处理

        nsolutions = np.where(nsolutions > boundary[1], boundary[1],
                             np.where(nsolutions < boundary[0], boundary[0], nsolutions))

        '''
        #  提取k个最好的点
        value = list(pool.map(func, solutions))
        index = np.argsort(value)[:k]
        solutions = solutions[[index]]
        '''
        itercount += 1
        
        #  计算k个中心点的标准差向量
        c = np.std(nsolutions, axis=0)
        #print(min(c))
        print(sigma0)
        if abs(max(c-sigma))<abs(sigma0):
            value = list(pool.map(func, nsolutions))
            badIndex=np.argmax(value)
            meanSolution=np.mean(nsolutions,axis=0)
            nsolutions[badIndex]=meanSolution
            c = np.std(nsolutions, axis=0)
            if abs(max(c))<abs(sigma0):
                sigma0/=2.0
                cov = np.diag(np.array([sigma0]*dim)**2)
        if sigma0 < critition or itercount > 10000:
            print('solutions:%s' % nsolutions[0])
            print('value:%s' % func(nsolutions[0]))
            print('itercount:%d' % itercount)
            break
        sigma=c
        centers=nsolutions



if __name__ == '__main__':
    try:
        qho(10, [3] * 100, [-100, 100],  fcts.griewank)
    except ValueError as err:
        print("OS error: {0}".format(err))
    except TypeError as err:
        print("Type error: {0}".format(err))
