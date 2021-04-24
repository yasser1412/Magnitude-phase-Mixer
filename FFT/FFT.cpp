#include<iostream>
#include<math.h>
#include<complex>
#include<vector> 
using namespace std;
#define pi 3.14159265359

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

main()
{
    int N = 1000;
    vector<complex<double>> signal;
    signal.reserve(N);

    for(int x=0; x<N; ++x)
    {
        auto temp = complex<double> (cos((2*pi/(1.0*N))*(x*1.0)), 0.0);
        signal.push_back(temp);
    }
    vector<complex<double>> FreqD = dft(signal); 
    for(int i=0; i<10; i++)
    {
        cout<<FreqD[i].real()<<"   "<<"j"<<FreqD[i].imag()<<endl;
    }

}

