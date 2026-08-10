#include <iostream>
#include <vector>
#include "signal_generator.h"
#include "bearing.geometry.h"
#include <librdkafka/rdkafkacpp.h>
#include "kafka_producer.h"

#include <csignal>

#include <thread>
#include <chrono>


static volatile sig_atomic_t run = 1;

static void sigterm(int sig) { run = 0; }

int main() {
    Bearing cwruBearing{"CWRU 6205", 9, 7.94, 39.04, 0.0};

    Frequencies frequencies = faultFrequencies(cwruBearing, 1.0);

    std::cout << "BPFO: " << frequencies.BPFO << std::endl;
    std::cout << "BPFI: " << frequencies.BPFI << std::endl;
    std::cout << "FTF: " << frequencies.FTF << std::endl;
    std::cout << "BSF: " << frequencies.BSF << std::endl;

    std::string topic = "features";

    RdKafka::Producer *producer = initProducer("kafka:9092");

    signal(SIGINT, sigterm);
    signal(SIGTERM, sigterm);

    while (run) {
        std::vector<double> impulse = generateImpulseTrain(frequencies.BPFO, 29.95, 20000, 0.2, 1.0);
        std::string turbineId = std::getenv("TURBINE_ID") ? std::getenv("TURBINE_ID") : "turbine-00";
        publishMessage(producer, topic, impulse, turbineId);
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    producer->flush(10000);
    delete producer;
}

