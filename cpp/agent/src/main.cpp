#include <iostream>
#include <vector>
#include "signal_generator.h"
#include "bearing.geometry.h"
#include <librdkafka/rdkafkacpp.h>
#include "kafka_producer.h"




int main() 
{
    Bearing cwruBearing{"CWRU 6205", 9, 7.94, 39.04, 0.0};

    Frequencies frequencies = faultFrequencies(cwruBearing, 1.0);

    std::cout << "BPFO: " << frequencies.BPFO << std::endl;
    std::cout << "BPFI: " << frequencies.BPFI << std::endl;
    std::cout << "FTF: " << frequencies.FTF << std::endl;
    std::cout << "BSF: " << frequencies.BSF << std::endl;

    std::vector<double> impulse = generateImpulseTrain(frequencies.BPFO, 29.95, 20000, 0.2, 1.0);

    std::string topic = "features";

    RdKafka::Producer *producer = initProducer("kafka:9092");
    publishMessage(producer, topic, impulse);

    producer->flush(10000);
    delete producer;
    /*
    std::vector<double> x = generateImpulseTrain(3.584, 29.95, 20000, 0.2, 1.0);

    for (int i = 0; i <= 60; i++)
    {
        std::cout << x[i] << std::endl;
    }
    */
}

