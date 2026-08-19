#pragma once

#include <string>
#include <atomic>
#include <librdkafka/rdkafkacpp.h>

RdKafka::KafkaConsumer* initConsumer(std::string brokers, std::string group_id);

enum faultType {
    NONE,
    BPFO,
    BPFI,
    BSF,
    FTF
};

void commandConsumerLoop(RdKafka::KafkaConsumer* consumer, const std::string& turbineId, std::atomic<int>& currentFault);
