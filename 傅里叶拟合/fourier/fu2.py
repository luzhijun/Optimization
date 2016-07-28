#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import math
from scipy import integrate
import cma
import numpy as np
import pickle
from multiprocessing import Pool
from scipy import ndimage
import matplotlib.pyplot as plt
l=2
D=22
N=100
result_list = []
PI=math.pi
def log_result(result):
    result_list.append(result)

def X2(x):
	return x*(x-1)*(x+1)+np.random.normal(0,0.5)

def initial():
	X=np.linspace(-l,l,N)
	#X=np.hstack((np.random.normal(0,2,10),X))
	#X.sort()
	Y=list(map(X2,X))
	Y[74]=-6
	dx=X[1]-X[0]
	dy=ndimage.gaussian_filter1d(Y, sigma=1, order=1, mode='wrap')/dx
	sy=np.cumsum(Y)*dx
	Ak=[1]
	for i in range(D-1):
		if i==0:
			continue
		Ak.append((-1)**i*2*(l/(i*PI)+(l/(i*PI))**3*(6-(i*PI)**2)))
	data={'X':X,'Y':Y,'dx':dx,'dy':dy,'sy':sy,'Ak':Ak}
	with open('data.tl','w') as f:
		pickle.dump(data,f,pickle.HIGHEST_PROTOCOL)

with open('data.tl','r') as f:
	data=pickle.load(f)

X=data['X']
Y=data['Y']
dx=data['dx']
dy=data['dy']
sy=data['sy']
Ak=data['Ak']

def FourierX2(An):	
	def fourier(x):
		s=0
		for  i,an in enumerate(An):
			if i==0:
				continue
			s+=an*math.sin(math.pi*i*x/l)
		return s
	return fourier

def FourierX2_(An):	
	def fourier(x):
		s=0
		for  i,an in enumerate(An):
			s+=(an*(i*math.pi/l)+(-1)**i*2*(l**2-1))*math.cos(math.pi*i*x/l)
		return s
	return fourier

def FourierX2__(An):	
	def fourier(x):
		s=0
		for  i,an in enumerate(An):
			if i==0:
				continue
			s+=-an*(math.cos(i*PI*x/l)+(-1)**(i+1))*l/(i*PI)
		return s
	return fourier

def MSE1(p):
	f=FourierX2(p[:-2])
	s=0
	for i in range(len(X)):
		s+=(Y[i]-f(X[i]))**2
	return s/len(X)
#导数
def MSE2(p):
	f=FourierX2_(p[:-2])
	X1=X[1:-1]
	dy1=dy[1:-1]
	s=0
	for i in range(len(X1)):
		s+=(dy1[i]-f(X1[i]))**2
	return s/len(X1)
#积分
def MSE3(p):
	f=FourierX2__(p[:-2])
	s=0
	for i in range(len(X)):
		s+=(sy[i]-f(X[i]))**2
	return s/len(X)

def WeightedMSEE(p):
	return MSE1(p)+MSE2(p)

def WeightedMSE(p):
	s=p[-2]+1
	return MSE1(p)/s+p[-2]*MSE2(p)/s

def WeightedMSE1(p):
	s=p[-2]+p[-1]+1
	return MSE1(p)/s+p[-2]*MSE2(p)/s+p[-1]*MSE3(p)/s

def cmaUser(mse,lamb,sigma=0.5,dim=D):
	func=lambda p:mse(p)
	lb=[-float('Inf')]*(dim-2)
	ub=[float('Inf')]*(dim-2)
	lb.append(0)
	ub.append(float('Inf'))
	lb.append(0)
	ub.append(float('Inf'))
	es = cma.CMAEvolutionStrategy(dim * [0], sigma,{'popsize':lamb,'boundary_handling': 'BoundTransform ','bounds': [lb,ub]})
	#es = cma.CMAEvolutionStrategy(dim * [0], sigma,{'popsize':lamb})
	while not es.stop() :
   		solutions = es.ask()
   		values=map(func,solutions)
   		es.tell(solutions, values)
	return es.result()[0],es.result()[1],lamb
#原
def draw1():
	p,y,lam= cmaUser(MSE1,15)
	print p,y
	f=FourierX2(p[:-2])
	f0=FourierX2(Ak[:-2])
	plt.figure()
	plt.plot(X,Y,'k.',label='original point')
	plt.plot(X,X*(X-1)*(X+1),'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc=0, numpoints=1)
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of y=x(x-1)(x+1)  \'s fourier')
	plt.show()
	plt.savefig('t1.pdf')
#导数
def draw2():
	p,y,lam= cmaUser(MSE2,15)
	print p,y
	f=FourierX2_(p[1:-2])
	f0=FourierX2_(Ak[1:-2])
	plt.figure()
	plt.plot(X,dy,'k.',label='original point')
	plt.plot(X,3*X**2-1,'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc=0, numpoints=1)
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	plt.xlabel('x')
	plt.ylabel('y\'')
	plt.title('fitting of  First order differential with y=x(x-1)(x+1) \'s fourier')
	plt.show()
	plt.savefig('t2.pdf')
#导数+原
def draw3():
	p,y,lam= cmaUser(WeightedMSEE,15)
	print p,y
	f=FourierX2(p[:-2])
	f0=FourierX2(Ak[:-2])
	plt.figure()
	plt.plot(X,Y,'k.',label='original point')
	plt.plot(X,X*(X-1)*(X+1),'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc=0, numpoints=1)
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of  y=x(x-1)(x+1) \'s fourier')
	plt.show()
	plt.savefig('m1.pdf')

#积分
def draw5():
	p,y,lam= cmaUser(MSE3,15)
	print p,y
	f=FourierX2__(p[:-2])
	f0=FourierX2__(Ak[:-2])
	plt.figure()
	plt.plot(X,sy,'k.',label='original point')
	plt.plot(X,((X**4-2*X**2)-(l**4-2*l**2))/4.0,'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc=0, numpoints=1)
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of  y=x(x-1)(x+1) \'s fourier with integral')
	plt.show()
	plt.savefig('t5.pdf')
#原+导数+积分
def draw6():
	p,y,lam= cmaUser(WeightedMSE1,15)
	print p,y
	f=FourierX2(p[:-2])
	f0=FourierX2(Ak[:-2])
	plt.figure()
	plt.plot(X,Y,'k.',label='original point')
	plt.plot(X,X*(X-1)*(X+1),'k',alpha=1,lw=1,label='original func')
	plt.plot(X,map(f0,X),'r',alpha=0.5,lw=3,label='original fourier line')
	plt.plot(X,map(f,X),'b',alpha=0.6,lw=3,label='fitting fourier line')
	plt.legend(loc=0, numpoints=1)
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of  y=x(x-1)(x+1) \'s fourier with integral')
	plt.show()
	plt.savefig('t6.pdf')


#多lambda
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
#多lambda
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
	plt.legend(loc=0, numpoints=1)
	leg = plt.gca().get_legend()
	ltext  = leg.get_texts()
	plt.setp(ltext, fontsize='small')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('fitting of  y=x(x-1)(x+1) \'s fourier')
	plt.show()
	plt.savefig('m2.pdf')

def main():
	#draw3()

	draw5()

	


if __name__=="__main__":
	main()

	















