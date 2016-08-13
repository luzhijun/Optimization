//公共参数
#define REPEAT 5
#define DIM 4  //设定目标函数的维数
#define PI 3.1415926
#define MAX 10    //搜索空间的最大值
#define MIN -10   //搜索空间的最小值
/////////////////////////////////////////
//qhoa算法参数
#define M_NUM   200   //每轮迭代每个种群需要搜索的次数，即M
#define K_NUM   20	  //种群个数，即每次迭代保留的近似最优解个数，即K
#define ACCURACY 0.000001		 //控制计算精度


//qpso算法参数
#define MAXITER 2000//最大迭代次数
#define POPSIZE 80//群体规模

//sa算法参数
#define MARKOVLENGTH 100000
#define DECAYSCALE 0.95
#define STEPFACTOR 0.02
#define TOLERANCE 0.0001
#define ACCEPTPOINT 0.0
#define TEMPERATURE 100


double func(double d[DIM]);
