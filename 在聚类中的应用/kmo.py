#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 12:16:28 2016

@author: Trucy
"""

import numpy as np
import cma
from collections import Counter
from numpy import linalg as LA
import time
import qho_engi1
import pso
import abca
import dea
import mqhoa_new1
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
                dataSet.append(list(map(float, l[:-1])))
                classify.append(int(l[-1]))
        self.originalData = np.array(dataSet)
        dataSet = self.normalize(self.originalData)
        self.sigma = LA.norm(np.var(dataSet, 0), 2)
        classify = np.array(classify)
        boundary = [np.min(dataSet, axis=0).tolist() *
                    self.k, np.max(dataSet, axis=0).tolist() * self.k]
        return dataSet, classify, boundary

    # 数值归一化
    def normalize(self, X):
        Xt = X.T
        Xt = np.array(
            list(map(lambda x: (x - min(x)) / (max(x) - min(x)), Xt)))
        return Xt.T

    def euclDistance(self, v1, v2):
        return LA.norm(v1 - v2, 2)

    def __purity(self, ls):
        c = Counter()
        for l in ls:
            c[l] += 1
        return c

    # init centroids with random samples
    def initCentroids(self):
        centroids = np.zeros((self.k, self.d))
        for i in range(self.k):
            index = int(np.random.uniform(0, self.n))
            centroids[i, :] = self.dataSet[index, :]
        return centroids

    # 计算距离矩阵
    def distanceMatrix(self, centroids):
        X = []
        for i in range(self.k):
            X.append(
                list(map(lambda x: self.euclDistance(centroids[i], x), self.dataSet)))
        return np.array(X)

    # 产生下一代中心点
    def kmeans(self, centroids, method):
        """
        args:
            methods: 1 返回下一代中心点
            methods: 0 返回适应度值
        """
        # step 1: init centroids
        # centroids = self.initCentroids()
        X = self.distanceMatrix(centroids)
        clusterAssment = np.argmin(X, axis=0)
        clusters = {}  # 正常聚类，存放索引
        zeroCluster = []  # 空聚类,存放索引
        # step 4: update centroids
        for j in range(self.k):
            # 在聚类中心j中的点
            pointsInCluster = np.nonzero(clusterAssment == j)[0]
            # 可能聚类中心没有相应的采样点
            if pointsInCluster.size == 0:
                print('第', j, '聚类中心没有找到采样点')
                zeroCluster.append(j)
            else:
                clusters[j] = pointsInCluster
        zeroClusterN = len(zeroCluster)
        # 如果存在不正常中心点
        if zeroClusterN != 0:
            ind = list(clusters.keys())
            nX = X[ind, ]
            badAssment = np.max(nX, axis=1)
            # 从正常聚类中找出zeroClusterN个最偏远的点
            if len(badAssment) > zeroClusterN:
                replaceInd = np.argpartition(-badAssment,
                                             zeroClusterN)[:zeroClusterN]
            else:
                replaceInd = [0] * zeroClusterN
            # 从正常聚类中抽出
            # 让空的聚类中心重定位到最差点
            for i in range(zeroClusterN):
                bi = np.argmax(nX[replaceInd[i]])
                pointsInCluster = clusters[ind[replaceInd[i]]]
                clusters[ind[replaceInd[i]]] = np.delete(
                    pointsInCluster, np.nonzero(pointsInCluster == bi)[0])
                centroids[zeroCluster[i]] = self.dataSet[bi]
        if method:
            for k, v in clusters.items():
                centroids[k] = np.mean(self.dataSet[v], axis=0)
            # 更新聚类中心点
            return centroids
        else:
            s = 0
            for k, v in clusters.items():
                s += sum(
                    list(map(lambda x: self.euclDistance(centroids[k], x), self.dataSet[v])))
            return s
    # 将结果写出来

    def k_near(self, centroids, filename):
        X = self.distanceMatrix(centroids)
        clusterAssment = np.argmin(X, axis=0)
        mark = clusterAssment.reshape((self.n, 1)) + 1
        data = np.hstack((self.originalData, mark))
        qho_engi1.dumpData(
            data, '/Users/Trucy/Documents/paper/di2src/实验/km/%s' % filename)
        return data

    # 根据x计算适应度值
    def __func(self, X):
        centroids = np.reshape(X, (self.k, self.d))
        # print(self.judge(centroids), self.SDbw(
        #    centroids), self.kmeans(centroids, 0))
        # return self.kmeans(centroids, 0)
        # return -self.judge(centroids)
        return self.SDbw(centroids)

    # 判断正确率根据F值
    def judge(self, centroids):
        #centroids = np.reshape(X, (self.k, self.d))
        X = self.distanceMatrix(centroids)
        clusterAssment = np.argmin(X, axis=0)
        # 原数据类别个数{1：12,2：34...}
        marks = self.__purity(self.classify)
        F = np.zeros((self.k, self.k))
        N = []
        for i in range(self.k):
            Ci = self.classify[np.nonzero(clusterAssment == i)[0]]
            res = self.__purity(Ci)
            Ni = len(Ci)
            N.append(Ni)
            print(res)
            for j, Nij in res.items():
                P = Nij / Ni
                R = Nij / marks[j]  # marks[j]对应Nj
                F[i - 1, j - 1] = 2 * P * R / (P + R)
        # print(F)
        maxF = np.max(F, axis=1)
        return maxF.dot(N) / self.n
    # 根据SDbw判断正确率=scat+deb_bw

    def SDbw(self, centroids):
        X = self.distanceMatrix(centroids)
        clusterAssment = np.argmin(X, axis=0)
        D = 0
        Cs = []
        for i in range(self.k):
            Ci = self.dataSet[np.nonzero(clusterAssment == i)[0]]
            ni = len(Ci)
            vari = 0
            for c in Ci:
                vari += (c - centroids[i])**2
            if ni != 0:
                D += LA.norm(vari / ni, 2)
            #D += LA.norm(np.var(Ci, 0), 2)
            Cs.append(Ci)
        # stdev = np.sqrt(D) / self.k
        stdev = np.sqrt(D) / self.k
        dens_bw = 0
        for i in range(self.k - 1):
            for j in range(i + 1, self.k):
                Ci, Cj = Cs[i], Cs[j]
                vi, vj = centroids[i], centroids[j]
                u = (vi + vj) / 2.0
                densityu, densityi, densityj = 0, 0, 0
                for x in Ci:
                    #print('u', self.euclDistance(x, u), stdev)
                    #print('i', self.euclDistance(x, vi), stdev)
                    if self.euclDistance(x, u) <= stdev:
                        densityu += 1
                    if self.euclDistance(x, vi) <= stdev:
                        densityi += 1
                for x in Cj:
                    if self.euclDistance(x, u) <= stdev:
                        densityu += 1
                    if self.euclDistance(x, vj) <= stdev:
                        densityj += 1
                #print(densityu, densityj, densityi, len(Cj), len(Ci))
                dens_bw += densityu / (max(densityj, densityi) + 1)
        # print(dens_bw)
        dens_bw /= (self.k * (self.k - 1) / 2.0)
        scat = D / self.sigma / self.k
        #print(dens_bw, scat)
        return dens_bw + scat

    def CMA(self):
        opts = cma.CMAOptions()
        opts['tolfun'] = 1e-6
        opts['tolfunhist'] = 1e-6
        opts['tolx'] = 1e-6
        opts['popsize'] = 10
        opts['maxiter'] = 30
        opts['bounds'] = self.boundary
        X0 = self.initCentroids()
        m = np.concatenate(self.kmeans(X0, 1), axis=0)
        # print(m)
        es = cma.CMAEvolutionStrategy(m, 0.7, opts)
        while not es.stop():
            # it += 1
            solutions = es.ask()
            es.tell(solutions, list(map(self.__func, solutions)))
            print(es.countiter, self.__func(solutions[0]))
            # SM.append(es.result()[0])
        es.logger.add()
        es.disp()
        es.result_pretty()
        X = es.result()[0]
        centroids = np.reshape(X, (self.k, self.d))
        print('F值', self.judge(centroids))
        print('sd', self.SDbw(centroids))
        self.k_near(centroids, 'cma1.tl')

    def cmm(self):
        X0 = self.initCentroids()
        up = self.boundary[0][0]
        down = self.boundary[1][0]
        X = qho_engi1.qho(self.__func, X0, (up - down) / 2,
                          20, boundary=[down, up], it=1000)
        print(self.judge(X))

    def k_means(self):
        X0 = self.initCentroids()
        old = self.kmeans(X0, 1)
        ov = np.concatenate(old, axis=0)
        it = 0
        while True:
            it += 1
            new = self.kmeans(old, 1)
            nv = np.concatenate(new, axis=0)
            if max(nv - ov) < 1e-6:
                break
            old = new
            ov = nv
        print(it, nv)
        print('F值', self.judge(nv))
        print('sd', self.SDbw(nv))
        print('适应度', self.kmeans(new, 0))

        self.k_near(new, 'kmeans.tl')

    def psoa(self):
        X, v = pso.pso(self.__func, self.boundary[0], self.boundary[1], maxiter=30,
                       minstep=1e-30, minfunc=1e-30, swarmsize=20, debug=False, omega=0.8, phip=2, phig=2)
        print(v)
        print(self.judge(X))
        centroids = np.reshape(X, (self.k, self.d))
        self.k_near(centroids, 'pso.tl')

    def abc(self):
        abcc = abca.ArtificialBeeSwarm(self.__func, 10, len(
            self.boundary[0]), np.array(self.boundary), 30)
        X, v = abcc.solve()
        centroids = np.reshape(X, (self.k, self.d))
        print('F值', self.judge(centroids))
        print('sd', self.SDbw(centroids))
        centroids = np.reshape(X, (self.k, self.d))
        self.k_near(centroids, 'abc.tl')

    def imqhoa(self):
        X0 = self.initCentroids()
        m = np.concatenate(self.kmeans(X0, 1), axis=0)
        X = mqhoa_new1.qho(10, m, self.boundary, self.__func, maxcount=100)
        centroids = np.reshape(X, (self.k, self.d))
        print('F值', self.judge(centroids))
        print('sd', self.SDbw(centroids))

        self.k_near(centroids, 'immqhoa1.tl')

    def cmmqhoa(self):
        X0 = self.initCentroids()
        m = np.concatenate(self.kmeans(X0, 1), axis=0)
        X = qho_engi1.qho(
            self.__func, m, 1, 10, boundary=self.boundary, it=50)
        # print(self.judge(X))
        centroids = np.reshape(X, (self.k, self.d))
        print('F值', self.judge(centroids))
        print('sd', self.SDbw(centroids))
        #self.k_near(centroids, 'cmmqhoa.tl')


if __name__ == "__main__":
    t = time.process_time()
    km = KMOptimzation("data/aggregation.txt", 7)
    # km.psoa()
    km.k_means()
    # km.psoa()
    # km.CMA()
    # km.abc()
    # km.imqhoa()
    # km.cmmqhoa()
    print(time.process_time() - t, 's')
