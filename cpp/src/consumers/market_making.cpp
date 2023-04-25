#include <iostream>
#include <cppkafka/cppkafka.h>
using namespace cppkafka;

using cppkafka::Configuration;
using cppkafka::Consumer;
using cppkafka::Message;
using cppkafka::Error;

class market_making {
public:
    market_making(int bidspread, int askspread,const Configuration& config)
        : bid_spread_(bidspread), ask_spread_(askspread), config_(config)
    {
        datafeed_ = std::make_shared<Consumer>(config_);
        std::cout << "Starting the strategy\n";
    }

    void run() {
        while (true) {
            Message msg = datafeed_->poll();

            if (!msg) {
                continue;
            }

            if (msg.get_error()) {
                if (msg.get_error().get_error() == RD_KAFKA_RESP_ERR__PARTITION_EOF) {
                    std::cout << "Reached end of partition\n";
                } else {
                    std::cout << "Error while consuming message: " << msg.get_error().to_string() << "\n";
                }
            } else {
                std::cout << "Received message: " << msg.get_payload() << "\n";
            }

            datafeed_->commit(msg);
        }
    }

public:
    std::string symbol_;
    std::string exchange_;
    int bid_spread_;
    int ask_spread_;
    cppkafka::Configuration config_;
    std::shared_ptr<Consumer> datafeed_;
};




int main(){

    Configuration conf = {
        { "metadata.broker.list", "localhost:9092" },
        { "group.id", "strategy-marketmaking-coinbase" },
        { "enable.auto.commit", false },
        { "auto.offset.reset", "latest" }
    };
    TopicPartition partition("coinbase-orderbook", 0); // ETH-USD
    market_making mm(10, 10, conf);
    mm.datafeed_->assign({ partition }); 
    mm.run();


}