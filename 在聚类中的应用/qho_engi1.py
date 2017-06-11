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
critition = 1e-6


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
    boundary = np.array(boundary)
    if lamb < 2:
        raise ValueError("lambda is too small!")
        return 1
    if not isinstance(1, type(lamb)):
        raise TypeError("lambda must be integer!")
    # 用于保存采样过程中sigma变化
    # SM = []
    pool = Pool()
    # 最好解比率，得出u
    radio = 2.0
    u = int(lamb / radio)
    # 权重常量
    alpha = 1.0 / sum((math.log((lamb + 1) / (2 * i))
                       for i in range(1, u + 1)))
    # 权重向量
    W = [alpha * math.log((lamb + 1) / (2 * i)) for i in range(1, u + 1)]
    # variance effective selection mass
    Ueff = 1.0 / sum([w**2 for w in W])
    dim = len(m)
    C1 = 2 / dim**2
    Cu = min(1 - C1, u / dim ** 2)
    Cc = 4.0 / (dim + 4)

    print('alpha:', alpha, 'Ueff:', Ueff, 'Cu:', Cu, 'Cc:', Cc)
    # 信息保留比率
    csigma = 4.0 / (dim + 4)
    # csigma = 0.7
    # cg0=I
    C = np.identity(dim)
    Pc = 0
    Psigma = np.zeros(dim)
    cov = np.eye(dim) * sigma
    solutions = np.random.multivariate_normal(m, cov, lamb)
    itercount = 0
    #SM = []
    while True:
        # 计算特征值向量D和正交矩阵B
        D, B = LA.eig(C)
        Dhalf = np.sqrt(np.abs(D))
        # 封装成MATRIX
        BM = np.matrix(B)
        # 简单边界处理
        for i in range(lamb):
            mark1 = solutions[i, :] < boundary[0]
            mark2 = solutions[i, :] > boundary[1]
            solutions[i, mark1] = boundary[0, mark1]
            solutions[i, mark2] = boundary[1, mark2]
        # 选出最好的u个点
        value = list(map(fct, solutions))
        index = np.argsort(value)[:u]
        solutions = solutions[index]
        nm = 0
        # 计算加权均值 new mean
        for i, s in enumerate(solutions):
            nm += W[i] * s
        '''
        if min(nm) < boundary[0]:
            nm[nm < boundary[0]] = boundary[0]
        if max(nm) > boundary[1]:
            nm[nm > boundary[1]] = boundary[1]
        if itercount % 50 == 0:
            SM.append(fct(solutions[0]))
        '''
        # 计算 covariance  matrix, C(g+1)
        Cg = np.zeros((dim, dim))
        for i in range(u):
            c = np.matrix(solutions[i] - m)
            Cg += W[i] * c.T * c
        # Rank-u-update   C  Cg  公式14
        # C = (1 - Cu) * C + Cu * Cg / sigma**2
        # Evolution Path
        Pc = np.matrix((1 - Cc) * Pc + np.sqrt(Cc * (2 - Cc)
                                               * Ueff) * (nm - m) / sigma)
        # 公式27
        C = (1 - C1 - Cu) * C + C1 * Pc.T * Pc + Cu * Cg / sigma**2

        # 更新迭代不成nmm，即论文中的p
        try:
            DM = np.matrix(np.diag(Dhalf))
            nmm = np.matrix(solutions[0] - m)
            nmm = BM * DM.I * BM.T * nmm.T
        except:
            print(Dhalf)
            raise LA.linalg.LinAlgError("Singular matrix!!")
        # nsigma=LA.norm(P,2)*sigma
        if itercount % 2 == 0:
            # SM.append(value[index[0]])
            print("iter", itercount, ': ', value[index[0]])
            # print("iter", itercount, ': ', fct(
            #   solutions[0]), 'sigma: ', sigma, 'nmm:', LA.norm(nmm, 2), 'D', LA.norm(Dhalf, 2))
        # print(C)
        # 更新迭代步长nsigma，保留一定的上一代步长信息
        # Psigma = (1 - csigma) * Psigma + \
        #    np.sqrt(csigma * (2 - csigma) * Ueff) * nmm
        nsigma = csigma * LA.norm(nmm, 2) + (1 - csigma) * sigma
        #nsigma = LA.norm(nmm, 2)
        # if max(Dhalf) < critition or itercount > it:
        # if value[index[0]] < critition or itercount > it:
        # if LA.norm(nm - m, 2) < critition or itercount > it:
        if itercount > it:
            print(Dhalf)
            print('solutions:%s' % solutions[0])
            print('value:%s' % value[index[0]])
            print('itercount:%d' % itercount)
            # print(len(SM))
            # dumpData(SM, "imqhoa.tl")
            return solutions[0]
            # return SM
        # 公式14 未展开形式
        solutions = np.random.multivariate_normal(nm, nsigma * C, lamb)
        # 更新均值、迭代步长
        m = nm
        sigma = nsigma
        itercount += 1


if __name__ == '__main__':
    try:
        '''
        for i in range(5):
            print(qho([5] * 20, 10, 200))
        '''
        dim = 100
        qho(fcts.ackley, [0] * dim, 0.5,
            20, boundary=[[-2.048] * dim, [2.048] * dim], it=1e5)
    except ValueError as err:
        print("OS error: {0}".format(err))
    except TypeError as err:
        print("Type error: {0}".format(err))
