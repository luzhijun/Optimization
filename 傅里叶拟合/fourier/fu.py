#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import math
import cma
import numpy as np
import pickle
from multiprocessing import Pool
from scipy import ndimage
import matplotlib.pyplot as plt
l=5
D=30

result_list = []
def log_result(result):
    result_list.append(result)

def X2(x):
	return x**2+np.random.normal(0,1)

X=np.linspace(-l,l,50)
#X=np.hstack((np.random.normal(0,2,10),X))
#X.sort()
Y=list(map(X2,X))
dx=X[1]-X[0]
dy=ndimage.gaussian_filter1d(Y, sigma=1, order=1, mode='wrap')/dx

Ak=[l**2/3.0]
for i in range(D-1):
    Ak.append((-1)**(i+1)*(2*l/(i+1.0)/math.pi)**2)

def FourierX2(An):	
	def fourier(x):
		s=0
		for  i,an in enumerate(An):
			s+=an*math.cos(math.pi*i*x/l)
		return s
	return fourier

def FourierX2_(An):	
	def fourier(x):
		s=0
		for  i,an in enumerate(An):
			if i==0:
				continue
			s+=an*(-i*math.pi/l)*math.sin(math.pi*i*x/l)
		return s
	return fourier

def MSE1(p):
	f=FourierX2(p)
	s=0
	for i in range(len(X)):
		s+=(Y[i]-f(X[i]))**2
	return s/len(X)

def MSE2(p):
	f=FourierX2_(p)
	s=0
	for i in range(len(X)):
		s+=(dy[i]-f(X[i]))**2
	return s/len(X)

def WeightedMSE(p):
	return MSE1(p)+MSE2(p)

def cmaUser(mse,lamb,sigma=0.5,dim=D):
	func=lambda p:mse(p)
	es = cma.CMAEvolutionStrategy(dim * [0], sigma,{'popsize':lamb})
	while not es.stop() :
   		solutions = es.ask()
   		values=map(func,solutions)
   		es.tell(solutions, values)
	return es.result()[0],es.result()[1],lamb

def draw1():
	p,y,= cmaUser(MSE1,15)
	print p,y
	f=FourierX2(p)
	f0=FourierX2(Ak)
	plt.figure()
	plt.plot(X,Y,'k.',label='original point')
	plt.plot(X,X**2,'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of  y=x^2 \'s fourier')
	plt.show()
	plt.savefig('t1.pdf')

def draw2():
	p,y,= cmaUser(MSE2,15)
	print p,y
	f=FourierX2_(p)
	f0=FourierX2_(Ak)
	plt.figure()
	plt.plot(X,dy,'k.',label='original point')
	plt.plot(X,2*X,'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y\'')
	plt.title('fitting of  First order differential with y=x^2 \'s fourier')
	plt.show()
	plt.savefig('t2.pdf')

def draw3():
	p,y,= cmaUser(WeightedMSE,15)
	print p,y
	f=FourierX2(p)
	f0=FourierX2(Ak)
	plt.figure()
	plt.plot(X,Y,'k.',label='original point')
	plt.plot(X,X**2,'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of  y=x^2 \'s fourier')
	plt.show()
	plt.savefig('t12.pdf')

def ls():
	pool=Pool()
	lds=[5,13,21,30,50,100]
	for l in lds:
		pool.apply_async(cmaUser,args=(WeightedMSE,l,),callback = log_result)
	pool.close()
	pool.join()
	print "finished"
	with open('rs.tl','w') as f:
		pickle.dump(result_list,f,pickle.HIGHEST_PROTOCOL)

def draw4():
	with open('rs.tl','r') as f:
		result_list=pickle.load(f)
	print result_list
	plt.figure()
	f0=FourierX2(Ak)
	plt.plot(X,Y,'k.',label='original point')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	for i,res in enumerate(result_list):
		p=res[0]
		f=FourierX2(p)
		plt.plot(X,map(f,X),'b',alpha=0.6,lw=2+i/2.0,label='fitting fourier line with lambda:%s'%res[2])
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of  y=x^2 \'s fourier')
	plt.show()
	plt.savefig('m2.pdf')

def main():
	draw4()

if __name__=="__main__":
	main()

	















