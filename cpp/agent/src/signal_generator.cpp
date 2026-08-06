#define _USE_MATH_DEFINES
#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include "signal_generator.h"

const int decay {1000};
const int fImpact {3000};

std::vector<double> generateImpulseTrain(double faultFreq, double shaftSpeed, int sampleRate, double noiseLevel, double durationSeconds)
{
    std::vector<double> signal(sampleRate * durationSeconds);

    double window = 5.0 / decay;
    int numSamples = window * sampleRate;

    std::vector<double> t;
    std::vector<double> impulse;
    
    for (int i = 0; i < numSamples; i++)
    {
        double x = i * window / (numSamples - 1);
        t.push_back(x);

        double value = exp(-decay * t[i]) * sin(2 * M_PI * t[i] * fImpact);
        impulse.push_back(value);
    }

    double step = sampleRate / (faultFreq * shaftSpeed);

    for (int i = 0; i < signal.size(); i += (int)round(step))
    {
        for (int j = 0; j < impulse.size() && (i + j) < signal.size(); j++)
        {
            signal[i + j] = impulse[j];
        }
    }

    /*
    std::mt19937 gen(std::random_device{}());
    std::normal_distribution<double> dist(0.0, noiseLevel);
    
    for (int i = 0; i < signal.size(); i++)
    {
        signal[i] += dist(gen);
    }
    */
    
    return signal;
}

