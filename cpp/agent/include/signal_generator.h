#pragma once
#include <vector>

std::vector<double> generateNoise(int sampleRate, double noiseLevel, double durationSeconds);

std::vector<double> generateImpulseTrain(double faultFreq, double shaftSpeed, int sampleRate, double noiseLevel, double durationSeconds);

