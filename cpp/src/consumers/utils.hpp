#pragma once
#include <cppkafka/consumer.h>
#include <cppkafka/topic_partition.h>
#include <nlohmann/json.hpp>
#include <fstream>

using namespace cppkafka;
using json = nlohmann::json;

Consumer get_orderbook_datafeed(std::string exchange, std::string symbol) {
    if (exchange == "binance") {
        std::ifstream config_file("binance_config.json");
        json data;
        config_file >> data;
        auto symbol_dict = data.get<std::map<std::string, int>>();
        auto it = symbol_dict.find(symbol);
        if (it == symbol_dict.end()) {
            throw std::runtime_error("Symbol in binance exchange is not found. Please input valid symbol");
        }
        Configuration conf = {
            { "metadata.broker.list", "localhost:9092" },
            { "group.id", "strategy-marketmaking-binance" },
            { "enable.auto.commit", false },
            { "auto.offset.reset", "latest" },
            { "max.poll.records", 1 }
        };
        Consumer consumer(conf);
        TopicPartition partition("binance-orderbook", it->second);
        consumer.assign({ partition });
        return consumer;
    }
    else if (exchange == "coinbase") {
        std::ifstream config_file("coinbase_config.json");
        json data;
        config_file >> data;
        auto symbol_dict = data.get<std::map<std::string, int>>();
        auto it = symbol_dict.find(symbol);
        if (it == symbol_dict.end()) {
            throw std::runtime_error("Symbol in coinbase exchange is not found. Please input valid symbol");
        }
        Configuration conf = {
            { "metadata.broker.list", "localhost:9092" },
            { "group.id", "strategy-marketmaking-coinbase" },
            { "enable.auto.commit", false },
            { "auto.offset.reset", "latest" },
            { "max.poll.records", 1 }
        };
        Consumer consumer(conf);
        TopicPartition partition("coinbase-orderbook", it->second);
        consumer.assign({ partition });
        return consumer;
    }
    else if (exchange == "kraken") {
        std::ifstream config_file("kraken_config.json");
        json data;
        config_file >> data;
        auto symbol_dict = data.get<std::map<std::string, int>>();
        auto it = symbol_dict.find(symbol);
        if (it == symbol_dict.end()) {
            throw std::runtime_error("Symbol in kraken exchange is not found. Please input valid symbol");
        }
        Configuration conf = {
            { "metadata.broker.list", "localhost:9092" },
            { "group.id", "strategy-marketmaking-kraken" },
            { "enable.auto.commit", false },
            { "auto.offset.reset", "latest" },
            { "max.poll.records", 1 }
        };
        Consumer consumer(conf);
        TopicPartition partition("kraken-orderbook", it->second);
        consumer.assign({ partition });
        return consumer;
    }
    else{
        throw std::runtime_error("Invalid Exchange, exchange connector is not implemented yet");
    }
}