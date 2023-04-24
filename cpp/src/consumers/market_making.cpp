#include <iostream>
#include <cppkafka/cppkafka.h>
using namespace cppkafka;

int main(){
    std::cout << "Hello i am a consumer " << std::endl;

    // Create the config
    Configuration config = {
        { "metadata.broker.list", "localhost:9092" },
        { "group.id", "strategy-marketmaking-binance" }
    };

    // Create the consumer
    Consumer consumer(config);
    TopicPartitionList partitions = { { "binance-orderbook", 0 } };
    consumer.assign(partitions);

    // Continuously poll for new messages
    while (true) {
        Message msg = consumer.poll();

        if (msg) {
            std::string payload = msg.get_payload();
            std::cout << "Received message: " << payload << std::endl;
        }
    }
}