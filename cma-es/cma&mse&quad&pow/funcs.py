#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
测试函数集
'''
import math
import numpy as np
#多项式函数,p为参数向量
def f1(p):
	f = np.poly1d(p)
	return f
#指数函数
def f2(p):
	return lambda x:p[0]*(math.exp(x/p[1])-1)

#噪点多项式函数
def f11(p):
	return lambda x:np.poly1d(p)(x)+np.random.normal(0,20)

#噪点指数函数
def f21(p):
	return lambda x:p[0]*(math.exp(x/p[1])-1)+np.random.normal(0,20)

#多项式函数mse
def mse1(p,x,y):
	f=f1(p)
	s=0
	for i in range(len(x)):
		s+=(y[i]-f(x[i]))**2
	return s/len(x)

#指数函数mse
def mse2(p,x,y):
	f=f2(p)
	s=0
	for i in range(len(x)):
		s+=(y[i]-f(x[i]))**2
	return s/len(x)

#多项式mpe
def mpe1(p,x,y):
	f=f1(p)
	s=0
	for i in range(len(x)):
		s+=((y[i]-f(x[i]))/y[i])**2
	return s/len(x)
	
#指数函数mpe
def mpe2(p,x,y):
	f=f2(p)
	s=0
	for i in range(len(x)):
		s+=((y[i]-f(x[i]))/y[i])**2
	return s/len(x)

#多项式mae
def mae1(p,x,y):
	f=f1(p)
	s=0
	for i in range(len(x)):
		s+=abs((y[i]-f(x[i]))/y[i])
	return s/len(x)

#指数mae
def mae2(p,x,y):
	f=f2(p)
	s=0
	for i in range(len(x)):
		s+=abs((y[i]-f(x[i]))/y[i])
	return s/len(x)

