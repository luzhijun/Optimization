#!usr/bin/env python
#encoding: utf-8
'''
用cma方法优化二次多项式函数与指数函数，g1,g2分别对应y垂直和百分比残差函数
最后绘制曲线
'''
__author__="luzhijun" 

import Ss
import funcs
import cma
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(12345)
np.set_printoptions(precision=4)


	
def cmaUser(dataSet,residualFunc,dim=3):
	x=dataSet[0]
	y=dataSet[1]
	func=lambda p:residualFunc(p,x,y)
	es = cma.CMAEvolutionStrategy(dim * [0], 0.5)
	while not es.stop():
   		solutions = es.ask()
   		es.tell(solutions, [func(p) for p in solutions])
    	es.logger.add()
    	es.disp()
	return es.result()[0]

def drawline(dataSet,realDataSet,setnum,dim=3):
	x=dataSet[0]
	y=dataSet[1]
	
	pmse=cmaUser(dataSet,funcs.mse1,dim)
	pmpe=cmaUser(dataSet,funcs.mpe1,dim)
	pmae=cmaUser(dataSet,funcs.mae1,dim)
	print "------------pmse:%s pmpe:%s pmae:%s---------"% (pmse,pmpe,pmae)
	if(setnum<3):
		ymse=list(map(funcs.f1(pmse),x))
		ympe=list(map(funcs.f1(pmpe),x))
		ymae=list(map(funcs.f1(pmae),x))
	else:
		ymse=list(map(funcs.f2(pmse),x))
		ympe=list(map(funcs.f2(pmpe),x))
		ymae=list(map(funcs.f2(pmae),x))

	plt.plot(realDataSet[0],realDataSet[1],c="black",lw=3,ls="-",alpha=0.6,label="real")
	plt.plot(x,ymse,c="red",lw=2,ls="-",alpha=0.5,label="mse")
	plt.plot(x,ympe,c="green",lw=2,ls="-",alpha=0.5,label="mpe")
	plt.plot(x,ymae,c="blue",lw=2,ls="-",alpha=0.5,label="mae")
	plt.scatter(x,y,alpha=0.3,marker=u'o',s=5,c=u'b')
	plt.legend(loc='best')
	if setnum>2:
		plt.xlim(-2,20)
		plt.ylim(-100,1000)
	else:
		plt.xlim(-2,25)
		plt.ylim(-50,1000)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of set %s' % setnum)

'''
#同时打印六幅图
plt.figure(1)
for i in range(6):
	plt.subplot(6,1,i+1)
	if(i<3):
		dim=3
	else:
		dim=2
	drawline(Ss.dataSet[i],Ss.realDataSet[i/3],i,dim)
plt.savefig(u'test1.pdf')
'''

#单独打印
plt.figure(1)
i=0
drawline(Ss.dataSet[i],Ss.realDataSet[i/3],i,3)
plt.savefig(u'fig1.pdf')
plt.figure(2)
i=1
drawline(Ss.dataSet[i],Ss.realDataSet[i/3],i,3)
plt.savefig(u'fig2.pdf')
plt.figure(3)
i=2
drawline(Ss.dataSet[i],Ss.realDataSet[i/3],i,3)
plt.savefig(u'fig3.pdf')
plt.figure(4)
i=3
drawline(Ss.dataSet[i],Ss.realDataSet[i/3],i,2)
plt.savefig(u'fig4.pdf')
plt.figure(5)
i=4
drawline(Ss.dataSet[i],Ss.realDataSet[i/3],i,2)
plt.savefig(u'fig5.pdf')
plt.figure(6)
i=5
drawline(Ss.dataSet[i],Ss.realDataSet[i/3],i,2)
plt.savefig(u'fig6.pdf')






