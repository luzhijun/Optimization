#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
测试funcs
'''
import funcs
import unittest
import math

class TestFucs(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	def test_f1(self):
		f=funcs.f1([2,1,0])
		self.assertEquals(f(1),3)
		self.assertEquals(f(0),0)
	def test_f2(self):
		f=funcs.f2([1,1])
		self.assertEquals(f(0),0)
	def test_mse1(self):
		om=funcs.mse1([2,1,0],[1,2,3],[3,10,21])
		self.assertEquals(om,0)
	def test_mse2(self):
		om=funcs.mse2([1,1],[0,0],[0,0])
		self.assertEquals(om,0)
	def test_mpe1(self):
		om=funcs.mpe1([2,1,0],[1,2,3],[3,10,21])
		self.assertEquals(om,0)
	def test_mpe2(self):
		om=funcs.mpe2([1,1],[1,2],[math.e-1,math.e**2-1])
		self.assertTrue(om<1e-16)
	def test_mae1(self):
		om=funcs.mae1([2,1,0],[1,2,3],[3,10,21])
		self.assertEquals(om,0)
	def test_mae2(self):
		om=funcs.mae2([1,1],[1,2],[math.e-1,math.e**2-1])
		self.assertTrue(om<1e-16)

if __name__ =='__main__':
	unittest.main()