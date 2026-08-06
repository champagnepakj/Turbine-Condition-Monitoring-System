#include <iostream>
#include <string>
#include <cmath>
#include "bearing.geometry.h"


Frequencies faultFrequencies(const Bearing& bearing, double shaftHz)
{
    Frequencies freqs;
    // Ballpass fault, outer race
    freqs.BPFO = ((bearing.nElements * shaftHz) / 2) * (1 - (bearing.elementsDiameter / bearing.pitchDiameter * cos(bearing.contactAngle)));
    //Ballpass fault, inner race
    freqs.BPFI = ((bearing.nElements * shaftHz) / 2) * (1 + (bearing.elementsDiameter / bearing.pitchDiameter * cos(bearing.contactAngle)));
    // Fundamental train frequency
    freqs.FTF = (shaftHz / 2) * (1 - (bearing.elementsDiameter / bearing.pitchDiameter * cos(bearing.contactAngle)));
    // Ball spin frequency
    freqs.BSF = ((bearing.pitchDiameter * shaftHz) / (2 * bearing.elementsDiameter)) * (1 - std::pow((bearing.elementsDiameter / bearing.pitchDiameter) * cos(bearing.contactAngle), 2));

    return freqs;
}
