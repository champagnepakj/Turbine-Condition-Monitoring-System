#pragma once
#include <string>

struct Bearing 
{
    std::string name                {};
    int         nElements           {};
    double      elementsDiameter    {};
    double      pitchDiameter       {};   
    double      contactAngle        {0.0};
};

struct Frequencies
{
    double BPFO;
    double BPFI;
    double FTF;
    double BSF;
};


Frequencies faultFrequencies(const Bearing& bearing, double shaftHz);
