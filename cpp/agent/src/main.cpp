#include <iostream>
#include <vector>
#include "signal_generator.h"
#include "bearing.geometry.h"
#include <librdkafka/rdkafkacpp.h>
#include "kafka_producer.h"
#include "kafka_consumer.h"

#include <csignal>

#include <thread>
#include <chrono>

#ifdef _WIN32
#include <winsock.h>
#else
#include <unistd.h>
#endif

volatile sig_atomic_t run = 1;

static void sigterm(int sig) { run = 0; }

std::atomic<int> current_fault_state{0};



int main() {
    Bearing cwruBearing{"CWRU 6205", 9, 7.94, 39.04, 0.0};

    Frequencies frequencies = faultFrequencies(cwruBearing, 1.0);

    std::cout << "BPFO: " << frequencies.BPFO << std::endl;
    std::cout << "BPFI: " << frequencies.BPFI << std::endl;
    std::cout << "FTF: " << frequencies.FTF << std::endl;
    std::cout << "BSF: " << frequencies.BSF << std::endl;

    std::string topic = "features";

    signal(SIGINT, sigterm);
    signal(SIGTERM, sigterm);

    std::string turbineId;
    if (std::getenv("TURBINE_ID")) {
        turbineId = std::getenv("TURBINE_ID");
    } else {
        char hostname[256];
        gethostname(hostname, sizeof(hostname));
        turbineId = std::string("turbine-") + hostname;
    }

    //RdKafka::Producer *producer = initProducer("kafka:9092");
    //RdKafka::KafkaConsumer *consumer = initConsumer("kafka:9092", turbineId);

    std::string broker = std::getenv("KAFKA_BROKER") ? std::getenv("KAFKA_BROKER") : "localhost:9094";
    RdKafka::Producer *producer = initProducer(broker);
    //RdKafka::KafkaConsumer *consumer = initConsumer(broker, turbineId);

    // std::ref forcing reference passing
    //std::thread commandThread(commandConsumerLoop, consumer, turbineId, std::ref(current_fault_state));

    while (run) {

        std::cout << "Loop iteration" << std::endl;

        int fault = current_fault_state.load();

        std::cout << "Fault state: " << fault << std::endl;

        
        std::vector<double> impulse;
        if (fault == BPFO) {
            impulse = generateImpulseTrain(frequencies.BPFO, 29.95, 20000, 0.2, 1.0);
        } else if (fault == BPFI) {
            impulse = generateImpulseTrain(frequencies.BPFI, 29.95, 20000, 0.2, 1.0);
        } else if (fault == BSF) {
            impulse = generateImpulseTrain(frequencies.BSF, 29.95, 20000, 0.2, 1.0);
        } else if (fault == FTF) {
            impulse = generateImpulseTrain(frequencies.FTF, 29.95, 20000, 0.2, 1.0);
        } else {
            std::cout << "Generating noise" << std::endl;
            // NONE — pure noise only, no impulse train
            impulse = generateNoise(20000, 0.2, 1.0);
        }

        std::cout << "About to publish" << std::endl;
        publishMessage(producer, topic, impulse, turbineId);
        std::cout << "Published" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    // Cleanup
    //commandThread.join();
    //consumer->close();
    //delete consumer;
    producer->flush(10000);
    delete producer;
}

