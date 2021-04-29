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

extern "C"
{
double calculate_errors(int N);
vector<complex<double>> create_array(int N);
vector<complex<double>> fft(vector<complex<double>> input);
vector<complex<double>> dft(vector<complex<double>> input);
}


double calculate_errors(int N)
{
    vector<complex<double>> signal = create_array(N);
    vector<complex<double>> FreqD = dft(signal);
    vector<complex<double>> FreqD1 = fft(signal);
    double real_error = 0;
    double imag_error = 0;
    
    for (int i = 0; i<N; i++)
    {
        real_error += pow((FreqD[i].real() - FreqD1[i].real()), 2.0);
        
        imag_error += pow((FreqD[i].imag() - FreqD1[i].imag()), 2.0);
    }
    return real_error , imag_error;
}

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


vector<complex<double>> fft(vector<complex<double>> input)
{
    int N = input.size();
    vector<complex<double>> copy = input;
    if(N==1) {return copy;}
    
    int M = N/2;
    
    vector<complex<double>> Xeven(M,0);
    vector<complex<double>> Xodd(M,0);
    
    for(int i=0; i<M; i++)
    {
        Xeven[i] = input[2*i];
        Xodd[i] = input[2*i+1]; 
    }
    vector<complex<double>> Feven(M,0);
    Feven = fft(Xeven);
    
    vector<complex<double>> Fodd(M,0);
    Fodd = fft(Xodd);

    vector<complex<double>> freqbins(N,0);
    for(int k=0; k!=N/2; k++)
    {   
        double angel = (-2*pi*k)/N;
        double CosA = cos(angel);
        double SinA = sin(angel);
        complex<double>temp(CosA, SinA);
        
        complex<double> cmplxexponential = temp*Fodd[k];
        
        freqbins[k] = Feven[k]+cmplxexponential;
        freqbins[k+N/2] = Feven[k]-cmplxexponential;
    }
    return freqbins;
}

vector<complex<double>> dft(vector<complex<double>> input)
{
    int N = input.size();
    
    complex<double> sum;
    vector<complex<double>> output;
    output.reserve(N);
    
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
        output.push_back(sum);
    }
    return output;
}

main( int argc, char *argv[] )
{
    int N = atoi(argv[1]);
    
    int operation = atoi(argv[2]);
    
    vector<complex<double>> signal = create_array(N);

    if (operation == 1)
    {
    vector<complex<double>> FreqD = dft(signal); 
    }
    
    if (operation == 2)
    {
    vector<complex<double>> FreqD1 = fft(signal); 
    }

}

