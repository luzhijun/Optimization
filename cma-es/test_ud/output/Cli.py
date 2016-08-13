#!usr/bin/env python
#encoding: utf-8
__author__="luzhijun"

import math,cma,time,logging


logging.basicConfig(level=logging.INFO,
                format='%(message)s',
                filename='cli.log',
                filemode='w')

def rosen(x, alpha=1e2):
    """Rosenbrock test objective function   x length>3"""
    sum=0
    for i in range(len(x)-1):
        sum+=alpha*math.pow((x[i+1]-x[i]*x[i]),2)+math.pow((1-x[i]),2)
    return sum



def main():
    dim=50
    t=[]
    count_iter=0
    es = cma.CMAEvolutionStrategy(dim * [0.3], 0.3)
    while not es.stop() :
        t.append(time.time())
        solutions = es.ask()
        logging.info('%s ask %.3f'%(count_iter,time.time()-t.pop()))
        t.append(time.time())
        aa=[rosen(p) for p in solutions]
        logging.info('%s calcu %.3f'%(count_iter,time.time()-t.pop()))
        t.append(time.time())
        es.tell(solutions, aa)
        logging.info('%s tell %.3f'%(count_iter,time.time()-t.pop()))
        count_iter+=1
    return es.result()[0]
if __name__ == '__main__':     
    main()


    











