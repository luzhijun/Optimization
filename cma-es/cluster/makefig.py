#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''
import pickle
from matplotlib import pyplot as plt



def fig():
    with open("data2.tl",'r') as f:
    	result_list=pickle.load(f)
    plts=[]
    length=len(result_list)
    for i in range(length):
        p1,=plt.plot(result_list[i][0])
        plts.append(p1)
        print('iter count:%s'%result_list[i][1])
        print result_list[i][2]
        print result_list[i][3]
        print result_list[i][4]
        print result_list[i][5]  
        print ''.join(['---']*20)
    plt.plot([0.003]*8000,'--')
    plt.ylim(0,0.003)
    plt.xlim(6000,8000)
    plt.ylabel('sigma')
    plt.xlabel('counter')
    plt.title('dim=100,popsize=120')
    plt.legend(plts,[result_list[i][5] for i in range(length)],loc=0,fontsize=10)
    #plt.show()
    plt.savefig("df2a.pdf")


if __name__ == '__main__':     
    #print cmaUser1(0.0001)
   fig()











