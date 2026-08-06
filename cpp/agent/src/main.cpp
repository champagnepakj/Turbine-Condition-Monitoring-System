#include <iostream>
#include <vector>
#include "signal_generator.h"

int main() {

    std::vector<double> x = generateImpulseTrain(3.584, 29.95, 20000, 0.2, 1.0);

    for (int i = 0; i <= 60; i++)
    {
        std::cout << x[i] << std::endl;
    }
}
