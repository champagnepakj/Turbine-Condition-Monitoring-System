#include <iostream>
#include <librdkafka/rdkafkacpp.h>
#include "kafka_consumer.h"
#include <csignal>

extern volatile sig_atomic_t run;

RdKafka::KafkaConsumer* initConsumer(std::string brokers, std::string group_id) {
    RdKafka::Conf *conf = RdKafka::Conf::create(RdKafka::Conf::CONF_GLOBAL);
    std::string errstr;

    // set brokers
    if (conf->set("bootstrap.servers", brokers, errstr) != RdKafka::Conf::CONF_OK) {
        std::cerr << errstr << std::endl;
        exit(1);
    }
    // set group.id
    if (conf->set("group.id", group_id, errstr) != RdKafka::Conf::CONF_OK) {
        std::cerr << errstr << std::endl;
        exit(1);
    }
    // set auto.offset.reset to "latest" (dont replay old commands)
    if (conf->set("auto.offset.reset", "latest", errstr) != RdKafka::Conf::CONF_OK) {
        std::cerr << errstr << std::endl;
        exit(1);
    }
    // create consumer with RdKafka::KafkaConsumer::create
    RdKafka::KafkaConsumer *consumer = RdKafka::KafkaConsumer::create(conf, errstr);
    if (!consumer) {
        std::cerr << "Failed to create consumer: " << errstr << std::endl;
        exit(1);
    }
    // subscribe to topic
    std::vector<std::string> topics = {"commands"};
    consumer->subscribe(topics);
    // return consumer
    delete conf;
    return consumer;
}

std::string extractField(const std::string& json, const std::string& field) {
    std::string search = "\"" + field + "\"";
    size_t pos = json.find(search);

    if (pos == std::string::npos) return "";
    
    pos = json.find(":", pos);
    pos = json.find("\"", pos) + 1;
    size_t end = json.find("\"", pos);
    
    return json.substr(pos, end - pos);
}

void commandConsumerLoop(RdKafka::KafkaConsumer* consumer, const std::string& turbineId, std::atomic<int>& currentFault) {
    
    while (run) {
        RdKafka::Message *msg = consumer->consume(1000);

        if (msg->err() == RdKafka::ERR__TIMED_OUT) {
            delete msg;
            continue;
        }

        if (msg->err() != RdKafka::ERR_NO_ERROR) {
            std::cerr << "Consumer error: " << msg->errstr() << std::endl;
            delete msg;
            continue;
        }

            std::cout << "Received message: " << static_cast<const char*>(msg->payload()) << std::endl;
            std::string payload(static_cast<const char*>(msg->payload()), msg->len());
            std::string msgTurbineId = extractField(payload, "turbine_id");
            std::string faultType = extractField(payload, "fault_type");

            if (msgTurbineId == turbineId) {
                if (faultType == "BPFO") currentFault = BPFO;
                else if (faultType == "BPFI") currentFault = BPFI;
                else if (faultType == "BSF") currentFault = BSF;
                else if (faultType == "FTF") currentFault = FTF;
                else currentFault = NONE;
            }

        delete msg;
    }
}
