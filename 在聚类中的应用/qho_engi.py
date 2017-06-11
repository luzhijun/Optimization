# encoding: utf-8

import numpy as np
import fcts
import pickle
import math

from numpy import linalg as LA
from multiprocessing import Pool

'''
qho
'''
__author__ = "luzhijun"
critition = 1e-100



def f1(b):
    p = np.array(b) / 100000
    s = b[0] * p[0]
    for x in [1, 2, 3, 4]:
        s += np.sum(b[:x + 1]) * (1 - np.sum(p[:x])) * p[x]
    s += (np.sum(b[:5]) + 100000) * (1 - np.sum(p[:5]))
    return s


def dumpData(x, filename):

    with open(filename, 'wb') as f:
        pickle.dump(x, f, pickle.DEFAULT_PROTOCOL)


def loadData(filename):
    with open(filename, 'rb') as f:
        x = pickle.load(f)
    return x


def qho(fct, m, sigma, lamb, boundary=[-10, 10], it=1000):
    '''《改进MQHOA算法用于全局优化》
        Args:
            fct:损失函数
            m:均值向量
            sigma:标准差向量
            lamb:种群数
            boundary:边界
            it:迭代次数
    '''
    # initialize
    if lamb < len(m):
        raise ValueError("lambda is too small!")
        return 1
    if not isinstance(1, type(lamb)):
        raise TypeError("lambda must be integer!")
    # 用于保存采样过程中sigma变化
    SM = []
    # pool = Pool()
    # 最好解比率，得出u
    radio = 5.0
    u = int(lamb / radio)
    # 权重常量
    alpha = 1.0 / sum((math.log((lamb + 1) / (2 * i + 2))
                       for i in range(u)))
    dim = len(m)
    # 信息保留比率
    # csigma = 4.0 / (dim + 4)
    csigma = 0.7
    cov = np.eye(dim) * sigma
    solutions = np.random.multivariate_normal(m, cov, lamb)
    itercount = 0

    while True:
        # 简单边界处理
        solutions = np.where(solutions > boundary[1], boundary[1],
                             np.where(solutions < boundary[0], boundary[0], solutions))
        # 选出最好的u个点
        value = list(map(fct, solutions))
        index = np.argsort(value)[:u]
        solutions = solutions[[index]]
        nm = 0
        # 计算加权均值 new mean
        for i, s in enumerate(solutions):
            nm += alpha * math.log((lamb + 1) / (2 * i + 2)) * s
        '''
        if min(nm) < boundary[0]:
            nm[nm < boundary[0]] = boundary[0]
        if max(nm) > boundary[1]:
            nm[nm > boundary[1]] = boundary[1]
        if itercount % 50 == 0:
            SM.append(fct(solutions[0]))
        '''
        # 计算 covariance  matrix
        C = np.zeros((dim, dim))
        for i in range(u):
            c = np.matrix(solutions[i] - m)
            C += alpha * math.log((lamb + 1) / (radio * i + 2)) * c.T * c
        # 计算特征值向量D和正交矩阵B
        D, B = LA.eig(C * 1e20)
        Dhalf = np.sqrt(np.abs(D)) / 1e10
        # 封装成MATRIX
        BM = np.matrix(B)
        # 更新迭代不成nmm，即论文中的p
        try:
            DM = np.matrix(np.diag(Dhalf))
            nmm = np.matrix(nm - m)
            nmm = BM * DM.I * BM.T * nmm.T
        except:
            print(D)
            print(Dhalf)
            raise LA.linalg.LinAlgError("Singular matrix!!")
        # nsigma=LA.norm(P,2)*sigma
        print(fct(solutions[0]))
        #print(C)
        # 更新迭代步长nsigma，保留一定的上一代步长信息
        nsigma = csigma * LA.norm(nmm, 1) + (1 - csigma) * sigma
        print(nsigma)
        if max(Dhalf) < critition or itercount > it:
            print(Dhalf)
            print('solutions:%s' % solutions[0])
            print('value:%s' % fct(solutions[0]))
            print('itercount:%d' % itercount)
            dumpData(SM, "imqhoa.tl")
            # return solutions[0]
            return fct(solutions[0])
        # 公式14 未展开形式
        solutions = np.random.multivariate_normal(nm, nsigma * C, lamb)
        # 更新均值、迭代步长
        m = nm
        sigma = nsigma
        itercount += 1
        SM.append(solutions[0])


if __name__ == '__main__':
    try:
        '''
        for i in range(5):
            print(qho([5] * 20, 10, 200))
        '''
        up = 10
        down = -up
        print(
            qho(fcts.griewank, [5] * 30, 5, 1000, boundary=[-10, 10], it=200))
    except ValueError as err:
        print("OS error: {0}".format(err))
    except TypeError as err:
        print("Type error: {0}".format(err))
