// compile first
// then run using ./FFT (N) (operation)   i.e. ./FFT 16 1
// operation: 1 for DFT , 2 for FFT
// N have to be a base of 2 (2^1, 2^2, 2^3,......)

#include<iostream>
#include<math.h>
#include<complex>
#include<vector> 
using namespace std;
#define pi 3.14159265359

// functions connected to python
extern "C"
{
double calculate_errors(int N);
vector<complex<double>> create_array(int N);
vector<complex<double>> fft(vector<complex<double>> input);
vector<complex<double>> ft(vector<complex<double>> input);
}

// calculate errors between ft and fft
double calculate_errors(int N)
{
    vector<complex<double>> signal = create_array(N);
    vector<complex<double>> FreqD = ft(signal);
    vector<complex<double>> FreqD1 = fft(signal);
    double error = 0;
    
    for (int i = 0; i<N; i++)
    {
        error += (FreqD[i].real() - FreqD1[i].real())*(FreqD[i].imag() - FreqD1[i].imag());
    }
    return error;
}

// create a cosine data vector with size N
vector<complex<double>> create_array(int N)
{   
    vector<complex<double>> signal;
    signal.reserve(N);
    double phase = 0.0;
    
    for(int x=0; x<N; ++x)
    {
        auto temp = complex<double> ( cos((2*pi/(1.0*N))*(x*1.0) + phase) , 0.0 );
        signal.push_back(temp);
    }
    return signal;
}

// Calculate FFT
vector<complex<double>> fft(vector<complex<double>> input)
{
    int N = input.size();
    vector<complex<double>> copy = input;
    // stop on reaching enough spliting
    if(N<=1) {return copy;}
    
    int M = N/2;
    
    vector<complex<double>> Xeven(M,0);
    vector<complex<double>> Xodd(M,0);
    // split even and odd
    for(int i=0; i<M; i++)
    {
        Xeven[i] = input[2*i];
        Xodd[i] = input[2*i+1]; 
    }

    // recursive part 
    vector<complex<double>> Feven(M,0);
    Feven = fft(Xeven);
    vector<complex<double>> Fodd(M,0);
    Fodd = fft(Xodd);
    
    // calculate DFT
    vector<complex<double>> fftArray(N,0);
    for(int k=0; k<N/2; k++)
    {   
        double angel = (-2*pi*k)/N;
        double CosA = cos(angel);
        double SinA = sin(angel);
        complex<double>temp(CosA, SinA);
        
        fftArray[k] = Feven[k]+ temp*Fodd[k];
        fftArray[k+N/2] = Feven[k]- temp*Fodd[k];
    }
    return fftArray;
}

// Calculate FT
vector<complex<double>> ft(vector<complex<double>> input)
{
    int N = input.size();
    
    complex<double> sum;
    vector<complex<double>> dftArray;
    dftArray.reserve(N);
    
    for(int k=0; k<N; k++)
    {
        sum = complex<double>(0,0);
        for(int n=0; n<N; n++)
        {
            double angel = (2*pi*k*n)/N;
            double CosA = cos(angel);
            double SinA = sin(angel);
            complex<double>temp(CosA, -SinA);
            
            sum += input[n] * temp;
        }
        dftArray.push_back(sum);
    }
    return dftArray;
}


main( int argc, char *argv[] )
{
    int N = atoi(argv[1]);
    
    int operation = atoi(argv[2]);
    
    vector<complex<double>> signal = create_array(N);
    
    if (operation == 1)
    {
    vector<complex<double>> FreqD = ft(signal); 
    }
    
    if (operation == 2)
    {
    vector<complex<double>> FreqD1 = fft(signal); 
    }
}

