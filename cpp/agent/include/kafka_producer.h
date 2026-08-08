#pragma once

#include <librdkafka/rdkafkacpp.h>

RdKafka::Producer* initProducer(std::string brokers);

bool publishMessage(RdKafka::Producer *producer, std::string topic, const std::vector<double>& signal);
