Please put cec14_func.cpp and input_data folder with your algorithm in the same folder. Set this folder as the current path.
1. run the following command in Matlab window:
   mex cec14_func.cpp -DWINDOWS
2. Then you can use the test functions as the following example:
   f = cec14_func(x,func_num); 
   here x is a D*pop_size matrix.
3. main.m is an example test code with PSO algorithm.

