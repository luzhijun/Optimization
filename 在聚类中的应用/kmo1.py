#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 12:16:28 2016

@author: Trucy
"""

import numpy as np
import cma
from collections import Counter
from operator import itemgetter
from numpy import linalg as LA
import time
import qho_engi1


class KMOptimzation(object):
    def __init__(self, filename, k):
        self.filename = filename
        self.k = k
        self.dataSet, self.classify, self.boundary = self.__makeData()
        self.n, self.d = self.dataSet.shape

    def __makeData(self):
        dataSet = []
        classify = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                l = line.strip().split(',')
                dataSet.append(list(map(float, l[1:])))
                classify.append(int(l[0]))
        dataSet = np.array(dataSet)
        classify = np.array(classify)
        boundary = np.min(dataSet, axis=0).tolist() * \
            self.k, np.max(dataSet, axis=0).tolist() * self.k
        return dataSet, classify, boundary
    # calculate Euclidean distance

    def euclDistance(self, vector1, vector2):
        return LA.norm(vector1 - vector2, 2)

    def __purity(self, ls):
        c = Counter()
        for l in ls:
            c[l] += 1
        print(c)
        return max(c.items(), key=itemgetter(1))[1]

    # init centroids with random samples
    def __initCentroids(self):
        centroids = np.zeros((self.k, self.d))
        for i in range(self.k):
            index = int(np.random.uniform(0, self.n))
            centroids[i, :] = self.dataSet[index, :]
        return centroids

    def __initialX(self):
        clusterAssment = np.zeros(self.n)
        X = []
        # step 1: init centroids
        centroids = self.__initCentroids()
        # print(centroids)
        # for each sample
        for i in range(self.n):
            minDist = 10000000.0
            minIndex = 0
            for j in range(self.k):
                distance = self.euclDistance(
                    centroids[j, :], self.dataSet[i, :])
                if distance < minDist:
                    minIndex = j
                    minDist = distance
            clusterAssment[i] = minIndex  # 采样点i归属中心点j

        # step 4: update centroids
        for j in range(self.k):
            # 在聚类中心j中的点
            pointsInCluster = self.dataSet[np.nonzero(clusterAssment == j)[0]]
            # 可能聚类中心没有相应的采样点
            print("第", j, "个聚类:")
            print(pointsInCluster)
            # 更新聚类中心点
            centroids[j, :] = np.mean(pointsInCluster, axis=0)
            X.extend(centroids[j, :])
        return X

    # 根据x计算适应度值
    def __func(self, X):
        centroids = np.reshape(X, (self.k, self.d))
        v = 0
        for i in range(self.n):
            minDist = 10000000.0
            for j in range(self.k):
                distance = self.euclDistance(
                    centroids[j, :], self.dataSet[i, :])
                if distance < minDist:
                    minDist = distance
            v += minDist
        return v
    # 判断正确率

    def __judge(self, X):
        centroids = np.reshape(X, (self.k, self.d))
        clusterAssment = np.zeros(self.n)
        Num = 0
        for i in range(self.n):
            minDist = 10000000.0
            minIndex = 0
            for j in range(self.k):
                distance = self.euclDistance(
                    centroids[j, :], self.dataSet[i, :])
                if distance < minDist:
                    minIndex = j
                    minDist = distance
            clusterAssment[i] = minIndex
        for j in range(self.k):
            pointsInCluster = self.classify[np.nonzero(clusterAssment == j)[0]]
            Num += self.__purity(pointsInCluster)
        return Num / self.n

    def User1(self):

        opts = cma.CMAOptions()
        opts['tolfun'] = 1e-1
        opts['tolfunhist'] = 1e-1
        opts['tolx'] = 1e-4
        opts['popsize'] = 15
        opts['maxiter'] = 100
        opts['bounds'] = self.boundary
        X0 = self.__initialX()
        print(X0)
        es = cma.CMAEvolutionStrategy(X0, 1, opts)
        while not es.stop():
            #it += 1
            solutions = es.ask()
            es.tell(solutions, list(map(self.__func, solutions)))
            # SM.append(es.result()[0])
        es.logger.add()
        es.disp()
        es.result_pretty()
        X = es.result()[0]
        print(self.__judge(X))

    def User(self):
        X0 = self.__initialX()
        up = self.boundary[0][0]
        down = self.boundary[1][0]
        X = qho_engi1.qho(self.__func, X0, (up - down) / 2,
                          20, boundary=[down, up], it=100)
        print(self.__judge(X))


if __name__ == "__main__":
    t = time.clock()
    km = KMOptimzation("wines.txt", 3)
    km.User1()
    print(t - time.clock())
