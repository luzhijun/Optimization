#include <math.h>
#include "canshu.h"

double func(double d[DIM])//Griewank
{
	double a=0,b=1,c=0;
	for(int i=0;i<DIM;i++)
	{
	a=a+d[i]*d[i];
	b=b*cos(d[i]/sqrt(i+1.0));
	}
	c=(1.0/4000.0)*a-b+1.0;
	return c;
}

////////////////////////////////////////////////////////////////
/*double func(double d[DIM])//Levy
{ 
	double a=0.0,b=0.0,c=0.0,z=0.0;
	for(int i=0;i<(DIM-1);i++)
	{
	a+=pow((d[i]-1)/4,2)*(1+10*pow(sin(3.1415926*((d[i]-1)/4+1)+1),2));	
	}	
	b=1+(d[0]-1)/4;
	z=pow(sin(2*3.1415926*(1+(d[DIM-1]-1)/4)),2);
	c=pow(sin(3.1415926*b),2)+a+pow((d[DIM-1]-1)/4,2)*(1+10*z);
	return c;
}
*/
/////////////////////////////////////////////////////////////

/*double func(double d[DIM])//Rastrigin
{
	double c=0.0;
	for(int i=0;i<DIM;i++)
	{
		c=c+d[i]*d[i]-10*cos(2.0*PI*d[i]);
	}
	c=c+10*DIM;
	return c;
}
*/
/////////////////////////////////////////////////////////////

/*double func(double d[DIM])//Rosenbrock
{
	double c=0.0;
	for(int i=0;i<(DIM-1);i++)
	{
		c=c+(100.0*(d[i+1]-d[i]*d[i])*(d[i+1]-d[i]*d[i])+(d[i]-1)*(d[i]-1));
	}
	return c;
}
*/
/////////////////////////////////////////////////////////////

/*double func(double d[DIM])//Dixon&Price    (0,100)
{
	double a=0.0,c=0.0;
	for(int i=1;i<DIM;i++)
	{
		c=c+(i+1.0)*(2.0*d[i]*d[i]-d[i-1])*(2.0*d[i]*d[i]-d[i-1]);
	}
	a=(d[0]-1.0)*(d[0]-1.0);
	c=a+c;
	return c;
}
*/
//////////////////////////////////////////////////////////////
/*
double func(double d[DIM])
{
	double c=0.0;
	c=(d[0]-1.0)*(d[0]-1.0)+2*(2*d[1]*d[1]-d[0])*(2*d[1]*d[1]-d[0]);
	return c;
}
*/
//////////////////////////////////////////////////////////////
/*
double func(double d[DIM])
{
	double c=0;
	c=abs(d[0])+(d[0]+d[1]+d[2]-2)*(d[0]+d[1]+d[2]-2)+(d[0]+2*d[1]+4*d[2]-3)*(d[0]+2*d[1]+4*d[2]-3)+(d[0]+3*d[1]+9*d[2]-5)*(d[0]+3*d[1]+9*d[2]-5)+(d[0]+4*d[1]+16*d[2]-6)*(d[0]+4*d[1]+16*d[2]-6);
	return c;
}
*/

///////////////////////////////////////////////////////////

/*double func(double d[DIM])//sphere
{
	double c=0;
	for(int i=0;i<DIM;i++)
	{
		c=c+d[i]*d[i];
	}
	return c;
}
*/

//////////////////////////////////////////////////////////
/*double func(double d[DIM])//Ackley
{
	double a=0.0,b=0.0,c=0.0;
	for(int i=0;i<DIM;i++)
	{
		a=a+d[i]*d[i];
		b=b+cos(2.0*3.14159*d[i]);
	}
	c=20.0+exp(1.0)-20.0*exp(-0.2*sqrt((1.0/DIM)*a))-exp((1.0/DIM)*b);
	return c;
}
*/
//////////////////////////////////////////////////////////

/*double func(double d[DIM])//Matyas
{
	double c=0.0;
	c+=0.26*(pow(d[0],2)+pow(d[1],2))-0.48*d[0]*d[1];
	return c;
}
*/
////////////////////////////////////////////////////////
//此函数未定义高维度函数
/*
double func(double d[DIM])//Easom
{
	double c=0.0;
	double b=-pow(d[0]-PI,2)-pow(d[1]-PI,2);
	c+=-cos(d[0])*cos(d[1])*exp(b);
	return c;

}
*/
/////////////////////////////////////////////////////////

/*double func(double d[DIM])//Beale
{
	double c=0.0;
	c+=pow(1.5-d[0]+d[0]*d[1],2)+pow(2.25-d[0]+d[0]*d[1]*d[1],2)+pow(2.625-d[0]+d[0]*pow(d[1],3),2);
	return c;
}
*/
/////////////////////////////////////////////////////////
/*
double func(double d[DIM])//Bohachevsky
{	
	double c=0.0;
	c+=pow(d[0],2)+2*pow(d[1],2)-0.3*cos(3*PI*d[0])-0.4*cos(4*PI*d[1])+0.7;
	return c;
}
*/
////////////////////////////////////////////////////////

/*double func(double d[DIM])//Booth
{	
	double c=0.0;
	c+=pow(d[0]+2*d[1]-7,2)+pow(2*d[0]+d[1]-5,2);
	return c;
}
*/
////////////////////////////////////////////////////////

/*double func(double d[DIM])//Michalewics
{
	double c=0.0,a=0.0;
	for(int i=0;i<DIM;i++)
	{
	a=-sin(d[i])*pow(sin((i+1)*d[i]*d[i]/PI),20);
	c+=a;
	}
	return c;

}
*/
///////////////////////////////////////////////////////

/*double func(double d[DIM])//Sumsquare
{
	double c=0.0;
	for(int i=0;i<DIM;i++)
	c+=(i+1)*pow(d[i],2);
	return c;

}
*/
/////////////////////////////////////////////////////

/*double func(double d[DIM])//Zakharov
{
	double c=0.0,a=0,b=0,l=0.0;
	for(int i=0;i<DIM;i++)
	{
		a+=pow(d[i],2);
	}
	for(int i=0;i<DIM;i++)
	{
		b+=0.5*(i+1)*d[i];

	}
	for(int i=0;i<DIM;i++)
	{
		l+=0.5*(i+1)*d[i];
	}
	c+=a+pow(b,2)+pow(l,4);
	return c;
}
*/
///////////////////////////////////////////////////////
/*double func(double d[DIM])//Schaffer
{
	double c=0.0;
	double a=0,b=0;
	a=pow(sin(sqrt(d[0]*d[0]+d[1]*d[1])),2)-0.5;
	b=pow(1.0+0.001*(d[0]*d[0]+d[1]*d[1]),2);
	c=-0.5+a/b;
	return c;

}
*/	
