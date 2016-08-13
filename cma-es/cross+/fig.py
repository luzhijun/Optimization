#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"
'''
cma restart test
'''

import numpy as np
import matplotlib.pyplot as plt
import os
plt.rc('figure', figsize=(16, 9))

import makeData as md

div=[1,4,13,14,22,49]



def drawHeatMap(data,path,dim,iternum):
    column_labels = range(dim)
    row_labels = range(dim)
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn,vmin=-1,vmax=1)
    plt.title("The %s  th iteration"%iternum)
    plt.axis([0, dim, 0, dim])
    cbar = fig.colorbar(heatmap, ticks=[-1, 0, 1])
    cbar.ax.set_yticklabels(['< -1', '0', '> 1'])# vertically oriented colorbar
    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
    
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.set_xticklabels(row_labels, minor=False)
    ax.set_yticklabels(column_labels, minor=False)
    plt.savefig(path)


def draw():
    data=md.loadData('result.tl')
    for n,(k,v) in enumerate(data.iteritems()):
        mat=v[2]['matrix']
        path='fig/fig_%s'%k
        os.mkdir(path)
        for i in range(0,len(mat),1):
            drawHeatMap(mat[i],os.path.join(path,'%d.png'%i),3*k,i*div[n])

def draw1():
    data=md.loadData('result1.tl')
    n=4
    k=25
    v=data[k]
    mat=v[3]['matrix']
    path='fig/fig_%s'%k
    if not os.path.exists(path):
        os.mkdir(path)
    for i in range(0,len(mat),2):
        drawHeatMap(mat[i],os.path.join(path,'%d.png'%int(i/2)),3*k,i*div[n])




if __name__ == '__main__':
    draw1()

