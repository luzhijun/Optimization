/*程序名称 :多尺度量子谐振子全局优化算法（目标函数为多维函数）
  主要思路：先从M_NUM*K_NUM个初始解中选择最优的K_NUM个，并分别将各维坐标和目标函数值保存在data[DIM][K_NUM]和f[K_NUM]中
  按照高斯分布在K_NUM个区域分别生成M_NUM个采样，进行迭代，将较优的K_NUM个值保存
  当每一维的标准差都小于预设的精度时迭代结束
  正态分布的标准差初始值为取值范围的1/2，以后每次标准差为上次的1/2
  data_temp[DIM][K_NUM]和f_temp[K_NUM]用于保持其与 data[DIM][K_NUM]和f[K_NUM]的一致性
*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "canshu.h"
#include "func.h"
//定义全局变量
double data[DIM][K_NUM];//全局数组，用于保存每次迭代时发现的K_NUM个较优解的各维坐标，每一行保存一个维度的坐标
double f[K_NUM];        //全局数组，用于保存每次迭代时发现的K_NUM个较小函数值
double data_temp[DIM][K_NUM];//全局数组，用于保存每次迭代后的data[DIM][K_NUM]
double f_temp[K_NUM];        //全局数组，用于保存每次迭代后的f[K_NUM]
double accuracy[DIM]={0};    //全局数组，用于保存各维的标准差
int num =0;//num变量用于保存总的迭代次数，此处初始化为0

 /* 求一个数组中的最大值*/
double biggest(double a[])
{
	double c=a[0];
	for(int i=1;i<DIM;i++)
	{
		while(a[i]>c)
		{
			c=a[i];
		}
	}
	return c;
}
/*交换函数，用于维护data[][]和data_temp的一致性*/
int switch_data()
{
	int i,j;
	for(i=0;i<DIM;i++)
	{
		for(j=0;j<K_NUM;j++)
		{
			data_temp[i][j]=data[i][j];
			f_temp[j]=f[j];
		}
	}
	return 1;
}

/* 产生属于（min，max）范围的随机数，随机数精度到小数点后6位*/
double AverageRandom(double min,double max)
{
	long minInteger =(long) (min*1000000);
    long maxInteger =(long) (max*1000000);
	long randInteger =rand();
	long diffInteger =maxInteger - minInteger;
	return (randInteger%diffInteger+minInteger)/1000000.0;
}
/*利用Box Muller法生成N(miu,sigma)的正态分布随机数*/
double Norm(double miu,double sigma)
{
	
	double x;
	double u1=rand()*1.0/RAND_MAX;
    double u2=rand()*1.0/RAND_MAX;
	x=miu+sigma*sqrt(-2.0*(log(u1)))*cos(2.0*PI*u2);
	return x;
	
}
double NormalRandom(double miu,double sigma)
{
	double norm_x;
	do{
	norm_x=Norm(miu,sigma);
        }while(norm_x<MIN||norm_x>MAX);
    return norm_x;
}

/* 计算迭代时各维坐标k个采样中心位置的标准差，sigma(k)*/
double function_Variance()
{
	double sum[DIM]={0.0}; //中间变量，在计算平均值和方差时保存中间运算值
	double aver[DIM]={0.0};//中间变量，在计算平均值和方差时保存中间运算值
	double sum1[DIM]={0.0};
	for(int i=0;i<DIM;i++)
	{
		for(int j=0;j<K_NUM;j++)
		{
			sum[i] +=data_temp[i][j];//将各维坐标求和
		}
		aver[i]=sum[i]/K_NUM;   //计算各维坐标的平均值
		for(int j=0;j<K_NUM;j++)
		{
			sum1[i] +=(data_temp[i][j]-aver[i])*(data_temp[i][j]-aver[i]);
		}
		accuracy[i]=sqrt(sum1[i]/K_NUM);
	}
return 1.0;
}
/*初始化运算，在定义域范围内随机分布产生K_NUM个DIM维高斯采样中心位置坐标，并计算其初始方差*/
int init_computing()
{
	int i,j;
	double temp[DIM];
	for(i=0;i<K_NUM;i++)
	{
		for(j=0;j<DIM;j++)
		{
			data_temp[j][i]=AverageRandom(MIN,MAX);
			data[j][i]=data_temp[j][i];//data与data_temp保持一致
			temp[j]=data_temp[j][i];
		}
		f[i]=func(temp);
	}
	function_Variance();//计算初始化时各维上的方差
	return 1;
}
/* 迭代运算主函数， 是本算法核心部分
 按照高斯分布生成M_NUM个解，与当前f[DIM]中的元素进行比较，如有更优解则替换
*/
int computing(double miu[DIM],double sigma)
{
	double datatemp[DIM];//临时保存采样点各维变量
	double rtemp;
	double stemp;
	int i=0,p=0,s=0;
	while(i<M_NUM)
	{
		for(int j=0;j<DIM;j++)//按照正态分布生成高维采样点位置
		{
			datatemp[j]=NormalRandom(miu[j],sigma);
		}
		stemp=f[0];
		s=0;
		p=1;
		while(p<K_NUM)//找出K_NUM个值中的最大值
		{
			if(stemp<f[p])
			{
			stemp=f[p];
			s=p;
			}
			p++;
		}
		rtemp=func(datatemp);
		if(rtemp<stemp)
		{
			for(int k=0;k<DIM;k++)
			{
				data[k][s]=datatemp[k];
			}
			f[s]=rtemp;
		}
		i++;
	}
	return 1;
}
//尺度为sigma的QHO迭代过程，MQHOA算法的核心迭代过程
int qho(double sigma)
{
	int p=0;
	while(p<K_NUM)
	{
		double data_c[DIM]={0.0};
		for(int j=0;j<DIM;j++)
		{
			data_c[j]=data_temp[j][p];//将各维坐标输出到data_c[]
		}
		computing(data_c,sigma);//进行一个采样区域迭代
		p++;
	}
	switch_data();
	function_Variance();	
	if(num%50==0)
		srand((int)time(0));
	num++;
	return 1;
}

/*主函数入口*/
int main(int argc,char* argv[])
{
	int rep;
	double avertime=0.0,avermin=0.0;
	for(rep=0;rep<REPEAT;rep++)//对目标函数重复REPEAT次计算求平均
	{
		srand((int)time(0));
		clock_t starttime,endtime;
		double totaltime;
		starttime=clock();
		int p=0,q=0;;
		double sigma=MAX-MIN;
		double smin=0.0;
		init_computing();
		/*外层循环，M收敛过程，按照设定好的尺度序列进行迭代，迭代尺度共d_num个*/
		do
		{
			/*内层循环，QHO收敛过程，所有维度中标准差最大的一维的标准差大于精度就继续迭代*/
			do
			{
				qho(sigma);
			}while(biggest(accuracy)>=sigma);
			sigma=sigma/2.0;
		}while(sigma>ACCURACY);
		/*获得K_NUM个较优解中使目标函数值最小的采样位置*/
		smin=f[0];
		p=1;
		while(p<K_NUM)
		{
			if(smin>f[p])
			{
				smin=f[p];
				q=p;
			}
			p++;
		}
		for(int s=0;s<DIM;s++)//打印K_NUM个较优解中的使目标函数值最小的采样位置
		{
			printf("%15.14f,",data[s][q]);
		}
		printf("min=%15.14f,%d,",smin,num);
		endtime=clock();
		totaltime=(double)(endtime-starttime)/CLOCKS_PER_SEC;
        printf("time=%15.14f\n",totaltime);
		avermin=avermin+smin;
		avertime=avertime+totaltime;
	}
	printf("avertime=%f,avermin=%15.14f\n",avertime/REPEAT,avermin/REPEAT);
	return 0;
}



