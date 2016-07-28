#!usr/bin/env python
#encoding: utf-8
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import sys
from optparse import OptionParser 

def opt_parser(args):

    parser = OptionParser()
    if len(args) < 1:  
        parser.error("incorrect number of arguments")
    parser.add_option('-i', '--input',
                      action='store', type='string', dest='infile',
                      help="file to plot")
    parser.add_option('-t', '--title',
                      action='store', type='string', dest='head',default='time sequence',
                      help="plot title")
    (options, args) = parser.parse_args(args)
    return options

def plot_files(infile,head):
	rs=pd.read_table(infile,sep='\s+',header=None)
	rs.index.names=['no.']
	rs.columns=['iter','step','values']
	#rs.sort_values(by='values')
	rsmean=rs.ix[1:,].groupby(['step']).mean()
	print 'mean value:'
	print '%s:%s'%(rsmean.index[0],rsmean.ix[0,1])
	print '%s:%s'%(rsmean.index[1],rsmean.ix[1,1])
	print '%s:%s'%(rsmean.index[2],rsmean.ix[2,1])
	rs.ix[1,['values']]=rsmean.ix[1,1]
	pt=pd.pivot_table(rs,values='values',index=['iter'],columns=['step'])
	ins=infile.split('.')
	plt.figure(1)
	pt.plot(title='time sequence:%s'%head,ylim=(0,0.02))
	plt.savefig(ins[0]+'0.pdf')
	pt.plot(kind='box',title='mean box:%s'%head,ylim=(0,0.02))
	plt.savefig(ins[0]+'1.pdf')

def main():
    opts = opt_parser(sys.argv[1:])
    plot_files(opts.infile,opts.head)
    return 0
if __name__ == '__main__':
    sys.exit(main())