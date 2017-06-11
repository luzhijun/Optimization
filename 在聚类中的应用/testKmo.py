#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 12:16:28 2016

@author: Trucy
"""
import unittest
import numpy as np
from kmo import KMOptimzation


class TestKMO(unittest.TestCase):

    def setUp(self):
        self.km = KMOptimzation("data/aggregation.txt", 7)

    def tearDown(self):
        pass

    def test_distanceMatrix(self):
        centroids = self.km.initCentroids()
        self.assertEqual(
            np.size(self.km.distanceMatrix(centroids), 0), 3)

    def test_initialX(self):
        centroids = self.km.initCentroids()
        print('boundary', self.km.boundary)
        print(self.km.kmeans(centroids, 0))

    def test_k_near(self):
        centroids = self.km.initCentroids()
        print(self.km.k_near(centroids).tolist())

    def test_judge(self):
        centroids = self.km.initCentroids()
        print(self.km.judge(centroids))

    def test_normalize(self):
        print(self.km.normalize(self.km.dataSet))

    def test_SDbw(self):
        # centroids = self.km.initCentroids()
        centroids = np.array([(8.76135886e-01, 2.72434582e-01), (9.13924322e-01, 6.70499845e-01), (1.29738187e-04, 2.51991144e-01),
                              (3.82118592e-01, 2.24755531e-01), (1.39660890e-02, 2.13665844e-03), (5.38911297e-01, 6.51908432e-01), (3.49811142e-01, 6.37659724e-01)])
        print(self.km.SDbw(centroids))

if __name__ == '__main__':
    unittest.main(defaultTest='TestKMO.test_SDbw')
