// sa.cpp : 定义控制台应用程序的入口点。
//
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "func.h"
#include "canshu.h"
/* Random Number from 0 to 1 */
double rnd()
{
    double r;
    r=(double) rand()/RAND_MAX;
    return r;
}
/* Global variable */
//double max[DIM];
double pre[DIM];
double next[DIM];
double prebest[DIM];
double best[DIM];

/* 产生属于（min，max）范围的随机数，随机数精度到小数点后6位*/
double AverageRandom(double min,double max)
{
	long minInteger =(long) (min*1000000);
    long maxInteger =(long) (max*1000000);
	long randInteger =rand();
	long diffInteger =maxInteger - minInteger;
	return (randInteger%diffInteger+minInteger)/1000000.0;
}
/*按Box Muller法生成正态分布N（miu,sigma）随机数*/
double Norm(double miu,double sigma)
{
	
	double x;
	double u1=rand()*1.0/RAND_MAX;
    double u2=rand()*1.0/RAND_MAX;
	x=miu+sigma*sqrt(-2.0*(log(u1)))*cos(2.0*PI*u2);
	return x;
	
}
/*将随机数限制在定义域范围内*/
double NormalRandom(double miu,double sigma)
{
	double norm_x;
	do{
	norm_x=Norm(miu,sigma);
        }while(norm_x<MIN||norm_x>MAX);
    return norm_x;
}

/* 在目标函数定义域随机生成一个初始采样点 */
void init()
{
   
    int k;
    for(k=0;k<DIM;k++)
    {
        pre[k]=AverageRandom(MIN,MAX);
		prebest[k]=best[k]=pre[k];
    }
}
/*主程序入口*/
int main(int argc, char * argv[])
{
    
	int rep;
	double avertime=0.0,avermin=0.0;
	for(rep=0;rep<REPEAT;rep++)//对目标函数重复REPEAT次计算求平均
	{
	const int markovlength=MARKOVLENGTH;
    const double decayscale=DECAYSCALE;//温度降低比例
  //  const double stepfactor=STEPFACTOR;
    const double tolerance=TOLERANCE;
	double acceptpoints=ACCEPTPOINT;
    double temperature=TEMPERATURE;
		//srand((int)time(0));
		clock_t starttime,endtime;
		double totaltime;
		starttime=clock();
		//通过时间,生成随机数种子
		srand((int)time(0));
		int i,iterator=0;//循环变量和迭代次数初始化
		int k;
		init();//生成初始采样点
		/*外层循环，降温过程*/
		do
		{
			acceptpoints=0.0;
			/*内层循环，等温过程*/
			for(i=0;i<markovlength;i++)
			{
				iterator++;
				for(k=0;k<DIM;k++)
				{
					next[k]=NormalRandom(pre[k],(MAX-MIN)/3.0);//按高斯邻域采生新的采样位置
				//	printf("next=%f\n",next[k]);
				//	next[k]=pre[k]+stepfactor*AverageRandom(MIN,MAX);
				}
					
				if (func(best)>func(next))
				{
					for(k=0;k<DIM;k++)
					{
						prebest[k]=best[k];
						best[k]=next[k];
					}
					acceptpoints=0.0;
				}
				/*Metropolis接收准则*/
				if (func(pre)>func(next))
				{
					for(k=0;k<DIM;k++)
						pre[k]=next[k];
					acceptpoints=0.0;
				}
				else
				{
					double change=-1*(func(next)-func(pre))/temperature;
					if(exp(change)>rnd())
					{
						for(k=0;k<DIM;k++)
							pre[k]=next[k];
						acceptpoints=0.0;
					}					
				}
				acceptpoints++;
				if(acceptpoints/markovlength>0.85)//多次未找到接受的新解，结束最优解查找
					break;
				/*重置随机数种子，获得更好的随机性*/
				if(iterator%50==0)
					srand((int)time(0));
                                
			}
			temperature=temperature*decayscale;//降低温度
		//	printf("temperature=%15.14f,best=%15.14f,tol=%15.14f\n",temperature,func(best),func(best)-func(prebest));
			if(acceptpoints/markovlength>0.85)
				break;
		}while(fabs(func(best)-func(prebest))>tolerance);//新解和旧解的差别小于tolerance时外层迭代结束

		 for(i=0;i<DIM;i++)
 		{
			printf("%15.14f,",best[i]);
		}
		printf("min=%15.14f,temper=%f",func(best),temperature);
		printf("%d,",iterator);
		endtime=clock();
		totaltime=(double)(endtime-starttime)/CLOCKS_PER_SEC;
        printf("time=%f\n",totaltime);
		avermin=avermin+func(best);
		avertime=avertime+totaltime;
	}
	printf("avertime=%f,avermin=%15.14f\n",avertime/REPEAT,avermin/REPEAT);
    return 0;
}

