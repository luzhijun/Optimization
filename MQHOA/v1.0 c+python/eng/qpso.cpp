#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include "time.h"
#include "math.h"
#include "canshu.h"
#include "func.h"
using namespace std;
//定义粒子结构体
struct particle
{
	double x[DIM];
	double pbest[DIM];
	double  bestfitness;
	double  fitness;
};
//全局变量定义
double irange_l=MIN;//位置初始化下界
double irange_r=MAX;//位置初始化下界
double XMIN=MIN;//搜索下界
double  XMAX=MAX;//搜索上界

void initiate(struct particle population[POPSIZE])
{
	int i,j;
	
	for(i=0;i<POPSIZE;i++)
	{
		for(j=0;j<DIM;j++)
		{
			population[i].x[j]=(rand()/(RAND_MAX+1.0)*(irange_r-irange_l)+irange_l);//生成irang_l到irang_r区间的随机数
			population[i].pbest[j]=population[i].x[j];//个体最好位置的初始化
		}
		population[i].fitness=func(population[i].x);//计算初始化位置的目标函数值
		population[i].bestfitness=population[i].fitness;//计算个体最好位置的目标函数值
	
	}

}
//获得全局最好的位置
int globalbest(struct particle population[POPSIZE])
{
	int i,flag;
	double  s=0;
	s=population[0].fitness;
	flag=0;
		for(i=1;i<POPSIZE;i++ )
		{
			if(population[i].fitness<s)
			{
				s=population[i].fitness;
				flag=i;
			}
			
		
		}
		
		return (flag);

}

int main()
{
	struct  particle swarm[POPSIZE];
	int i,j,k,t,g,run;
	double a,mbest[DIM],tmp,fi1,fi2,u,v,z,b,p;
	double data[REPEAT],sum,avg;
	double gbest[DIM];
	double minimum;
	srand((unsigned)time(NULL));
	sum=0;
	double	sumt=0;
	for(run=0;run<REPEAT;run++)
	{
	
		clock_t starttime,endtime;
		starttime=clock();
	
		for(j=0;j<DIM;j++)
			mbest[j]=0;
		initiate(swarm);
		g=globalbest(swarm);
		for(k=0;k<DIM;k++)
			gbest[k]=swarm[g].pbest[k];
		minimum=swarm[g].bestfitness;
		for(t=0;t<MAXITER;t++)
		{	
				for(k=0;k<DIM;k++)
			   { tmp=0;
				for(i=0;i<POPSIZE;i++)
				tmp=tmp+swarm[i].pbest[k];
				mbest[k]=tmp/POPSIZE;
			}
			a=(1.0-0.5)*(MAXITER-t)/MAXITER+0.5;
			for(i=0;i<POPSIZE;i++)
			{
				for(k=0;k<DIM;k++)
				{
					fi1=rand()/(RAND_MAX+1.0);
					fi2=rand()/(RAND_MAX+1.0);
					p=(fi1*swarm[i].pbest[k]+fi2*gbest[k])/(fi1+fi2);
					u=rand()/(RAND_MAX+1.0);
					b=a*fabs(mbest[k]-swarm[i].x[k]);
					v=log(1/u);
					z=rand()/(RAND_MAX+1.0);
					
					if(z<0.5)
						swarm[i].x[k]=(p+b*v);
					else
						swarm[i].x[k]=(p-b*v);
						
					if(swarm[i].x[k]<XMIN)
						swarm[i].x[k]=XMIN;
					if(swarm[i].x[k]>XMAX)
						swarm[i].x[k]=XMAX;
				}
			
				swarm[i].fitness=func(swarm[i].x);
				if(swarm[i].fitness<swarm[i].bestfitness)
				{
				for(k=0;k<DIM;k++)
					swarm[i].pbest[k]=swarm[i].x[k];
					swarm[i].bestfitness=swarm[i].fitness;
				}
				if(swarm[i].bestfitness<minimum)
				{
					for(k=0;k<DIM;k++)
					gbest[k]=swarm[i].pbest[k];
					minimum=swarm[i].bestfitness;
				}
			}
        }

		endtime=clock();
		for(int i=0;i<DIM;i++)
	           printf("%15.14f,",gbest[i]);
		printf("min=%15.14f",minimum);
		cout<<"time:"<<(double)(endtime-starttime)/CLOCKS_PER_SEC<<"s"<<endl;
		data[run]=minimum;
		sum=sum+minimum;
		sumt+=(double)(endtime-starttime)/CLOCKS_PER_SEC;
	}
	avg=sum/REPEAT;
	cout<<"avgvalue= "<<avg<<" avgtime= "<<sumt/REPEAT<<"s"<<endl;
}	
	
