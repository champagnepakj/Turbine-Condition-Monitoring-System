
#include <iostream>
#include <string>
#include <csignal>
#include <cstdlib>
#include <cstdio>

#include <librdkafka/rdkafkacpp.h>

#include "kafka_producer.h"

// Example code: https://github.com/confluentinc/librdkafka/blob/master/examples/producer.cpp

class ExampleDeliveryReportCb : public RdKafka::DeliveryReportCb {
public:
    void dr_cb(RdKafka::Message &message) {
        if (message.err())
            std::cerr << "% Message delivery failed: " << message.errstr() << std::endl;
        else
            std::cerr << "% Message delivered to topic: " << message.topic_name()
                      << " [" << message.partition() << "] at offset "
                      << message.offset() << std::endl;
    }
};


RdKafka::Producer* initProducer(std::string brokers) {

    // Create conf 
    RdKafka::Conf *conf = RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL);

    std::string errstr;

    // set the broker bootstrap.servers
    if (conf->set("bootstrap.servers", brokers, errstr) != RdKafka::Conf::CONF_OK) {
        std::cerr << errstr << std::endl;
        exit(1);
    }

    // set delivery callback
    static ExampleDeliveryReportCb ex_dr_cb;

    if (conf->set("dr_cb", &ex_dr_cb, errstr) != RdKafka::Conf::CONF_OK) {
        std::cerr << errstr << std::endl;
        exit(1);
    }

    // create producer
    RdKafka::Producer *producer = RdKafka::Producer::create(conf, errstr);
    if (!producer) {
        std::cerr << "Failed to create a producer: " << errstr << std::endl;
        exit(1);
    }
    // delete conf
    delete conf;

    // return producer
    return producer;
}


bool publishMessage(RdKafka::Producer *producer, std::string topic, const std::vector<double>& signal) {
    
    RdKafka::ErrorCode err = producer->produce(
        topic,
        RdKafka::Topic::PARTITION_UA,
        RdKafka::Producer::RK_MSG_COPY,
        const_cast<char*>(reinterpret_cast<const char*>(signal.data())), signal.size() * sizeof(double),
        NULL, 0,
        0,
        NULL,
        NULL);

    if (err != RdKafka::ERR_NO_ERROR) {
        std::cerr << "% Failed to produce to topic " << topic << ": " << RdKafka::err2str(err) << std::endl;
        if (err == RdKafka::ERR__QUEUE_FULL) {
            producer->poll(1000);
        }
        return false;
    }

    producer->poll(0);
    return true;
}


