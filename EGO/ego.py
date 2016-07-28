#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import cma
import numpy as np
from numpy import linalg as LA
import pickle
import math
from multiprocessing import Pool

PI=math.pi
D=1
FN='haha.tl'

def func(X):
    return sum(X**2)

def dumpData(a,b,filename):
    x=(b - a) * np.random.random_sample((D,100)) + a
    with open(filename,'w') as f:
        pickle.dump(x,f,pickle.HIGHEST_PROTOCOL)

def loadData(size,filename):
    with open(filename,'r') as f:
        x=pickle.load(f)
    map(np.random.permutation,x)
    sample=np.array(np.random.permutation(x)[:size])
    sample=sample[:,:size]
    sample.sort()
    return sample

def distance(theta,p,xi,xj):
    s=0
    dim=len(xi)
    for d in range(dim):
        s+=theta[d]*pow(abs(xi[d]-xj[d]),p[d])
    return s

def corr(theta,p,xi,xj):
    return math.exp(-distance(theta,p,xi,xj))

def corrMartrix(x,theta,p):
    j=x.shape[1]
    CM=np.empty([j,j],dtype=np.float64)
    for m in range(j):
        for n in range(j):
            CM[m][n]=corr(theta,p,x[:,m],x[:,n])
    return np.asmatrix(CM)

def likelihood(x,theta,p):
    n=x.shape[1]
    y=func(x)
    Y=np.asmatrix(y).T
    OneT=np.matrix([1]*n)
    One=OneT.T
    C=corrMartrix(x,theta,p)
    CI=C.I
    mu=OneT*CI*Y/(OneT*CI*One)
    sigma_2=((Y-One*mu).T*CI*(Y-One*mu))/n
    return -1.0/(pow((2*PI*sigma_2),n/2.0)*LA.det(C)**0.5)*math.exp(((Y-One*mu).T*CI*(Y-One*mu))/(-2*sigma_2))

def getMu(x,theta,p):
    n=x.shape[1]
    y=func(x)
    Y=np.asmatrix(y).T
    OneT=np.matrix([1]*n)
    One=OneT.T
    C=corrMartrix(x,theta,p)
    CI=C.I
    mu=OneT*CI*Y/(OneT*CI*One)
    return mu

def decorateLikeihood(filename,size=50):
    X=loadData(size,filename)
    k=len(X)
    def MaxLikelihood(x):  
        theta=x[:k]
        p=x[k:]
        return likelihood(X,theta,p)
    return MaxLikelihood


def predict(filename,size,lamb,sigma=0.5):
    F=decorateLikeihood(filename,size)
    #pool=Pool()
    es = cma.CMAEvolutionStrategy(2*D * [0], sigma,{'popsize':lamb})
    while not es.stop():
        X = es.ask()
    #    es.tell(X, pool.map_async(F, X).get()) 
        es.tell(X,map(F,X))
    return es.result()[0],es.result()[1]



class LHS(object):
    proportion=0.01
    def __init__(self,num,boundary,dim,function):
        if function in [None,'']:
            self._function=func
        else:
            self._function=function
        self.num=num
        self.boundary=boundary
        self.dim=dim
        self.H=int(pow(self.num/LHS.proportion,1.0/self.dim))

    @staticmethod
    def func(x):
        '''
        默认方法
        '''
        return x**2
    @property    
    def boundary(self):
        return self._boundary

    @boundary.setter
    def boundary(self,b):
        if not b or type(b) !=list:
            raise ValueError('boundary must be a list')
        self._boundary=b

    @property    
    def num(self):
        return self._num

    @num.setter
    def num(self,num):
        if not isinstance(num, int):
            raise ValueError('number must be an integer!')
        if num<0 or  num >1000:
            raise ValueError('score must between 0 ~ 1000!')
        self._num=num

    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self,dim):
        if not isinstance(dim, int):
            raise ValueError('number must be an integer!')
        if dim<0 or  dim>200:
            raise ValueError('score must between 0 ~ 1000!')
        self._dim=dim

    def sample(self):
        bd=np.array(self.boundary)
        hc=np.random.randint(self.H,size=(self.num,self.dim))+0.5
        unit=(bd[1]-bd[0])/self.H
        hcv=np.dot(unit,hc)
        return hcv.transpose()


def main():

    dumpData(-10,10,FN)
    print predict(FN,10,20)



if __name__ == '__main__':     
    main()
    















