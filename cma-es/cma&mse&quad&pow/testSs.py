#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
根据测试数据集画图
'''
import Ss
import matplotlib.pyplot as plt

plt.figure(1)
for i in range(6):
	S=Ss.dataSet[i]
	plt.subplot(6,2,2*i+1)
	plt.scatter(S[0],S[1],alpha=0.3,marker=u'o',s=5,c=u'b')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('scatter of points set%s'%i)
	if i>2:
		plt.xlim(-2,20)
		plt.ylim(-80,1000)
	else:
		plt.xlim(-2,25)
		plt.ylim(-50,1000)
	plt.subplot(6,2,2*(i+1))
	plt.hist(S[0], 10, normed=1, facecolor='green', alpha=0.5)
	plt.xlabel('x')
	plt.ylabel('Probability')
	plt.title('Histogram of x')
plt.show()