#include<iostream>
#include<math.h>
#include <complex> 
using namespace std;
#define pi 3.14159265359

int main()
{
    double *inputArray; //array for input data (t-domain)
    int inputlength; //inputArray length
    int N = 10000; //number of samples

    //complex<long double> output[inputlength]; //{{real1, imag1},{real2, imag2},........} (array size have to be constant)
    
    long double *outputReal = new long double[inputlength]; //define real part of the fourier transform 
    long double *outputImag = new long double[inputlength]; //define real part of the fourier transform 

    // DFT function
    for(int k = 0; k<inputlength; k++)
    {
        //output[k] = {0,0};
        
        outputReal[k] = 0;
        outputImag[k] = 0;

        for(int n = 0; n<N; n++)
        {
            long double angel = (2*pi*k*n)/N;
            long double CosA = cos(angel);
            long double SinA = sin(angel);

            //output[k] = {inputArray[k]*CosA, inputArray[k]*SinA};
            
            outputReal[k] += inputArray[k]*CosA;
            outputImag[k] += inputArray[k]*SinA;
        }
    }
    // End of DFT Function

}