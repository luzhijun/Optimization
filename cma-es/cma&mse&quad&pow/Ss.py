#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
产生数据集合，dataSet[0:3]使用多项式函数产生噪点数据；dataSet[3:6]使用指数函数产生噪点数据；
realDataSet[0]存放多项式函数产生真实数据，realDataSet[1]存放指数函数产生真实数据
'''
import funcs
import numpy as np

x1=np.linspace(0,20,150)
x2=np.hstack((np.random.exponential(5,300),x1))
x2.sort()
x3=np.hstack((np.random.exponential(1,300),x1))
x3.sort()
x4=np.linspace(0,20,150)
x5=np.hstack((np.random.exponential(5,300),x4))
x5.sort()
x6=np.hstack((np.random.exponential(1,300),x4))
x6.sort()

dataSet=[]
p1=[2,1,0]  #多项式函数参数
p2=[0.5,2]	#指数函数参数
y1=list(map(funcs.f11(p1),x1))
dataSet.append([x1,y1])
y2=list(map(funcs.f11(p1),x2))
dataSet.append([x2,y2])
y3=list(map(funcs.f11(p1),x3))
dataSet.append([x3,y3])
y4=list(map(funcs.f21(p2),x4))
dataSet.append([x4,y4])
y5=list(map(funcs.f21(p2),x5))
dataSet.append([x5,y5])
y6=list(map(funcs.f21(p2),x6))
dataSet.append([x6,y6])

realDataSet=[]
y1r=list(map(funcs.f1(p1),x1))
realDataSet.append([x1,y1r])
y2r=list(map(funcs.f2(p2),x4))
realDataSet.append([x4,y2r])


