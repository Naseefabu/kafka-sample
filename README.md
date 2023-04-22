
# Event-Driven Algorithmic Trading using Kafka
This project is an event-driven algorithmic trading system implemented using Kafka, which receives raw exchange data via WebSockets, parses and normalizes order book events, and publishes those events via Kafka topics. The system is designed to be highly scalable and distributed, with multiple producers running on different AWS regions publishing order book data to consumers (strategies). 

# Getting Started 

## Prerequisites
  * Kafka and Zookeeper installed and running on your local machine or any other machine (for fault tolerance).
  * Install ccxtpro

## Usage 
  ### Step 1: Start ZooKeeper and Kafka Broker
  1. To start ZooKeeper, navigate to the Kafka directory and run the following command:
  ```
  bin/zookeeper-server-start.sh config/zookeeper.properties
  ```
  2. Next, start the Kafka broker by running the following command
  ```
  JMX_PORT=8004 bin/kafka-server-start.sh config/server.properties 
  ```

  ### Step 2: Create Symbols Partition Map
  1. Create a symbols partition map for each exchange in the following format:

    binance_config.json :
    ```
      {
      "SOL/USDT": 0,
      "APE/USD": 1
      }
    ```
    bitfinex_config.json :
    ```
      {
      "ETH/BTC": 0,
      "ETH/USDT": 1
      }
    ```
    The symbols partition maps is an essential aspect of this project. It's like a JSON file inside the project directory that tells you which partition ID does a specific symbol takes in a particular topic. For example, in the binance-orderbook topic, we may have a lot of partitions based on symbols in the Binance exchange, so the partition map will tell you what symbol and its partition ID so that consumers can identify them easily.

### 3. The orderbook topic format for each exchange is as follows:

    exchangename-orderbook

    For example:
    binance-orderbook
    coinbase-orderbook
    bitmex-orderbook

### 4. This project uses ccxt pro for websocket feed.

### 5. There are multiple producers in this project, such as binance_producer.py, coinbase_producer.py, and bitmex_producer.py. For best performance, it is recommended to run these producers in their own AWS regions where the exchange servers are located.









## Architecture Overview

The system is built on top of the Kafka message broker, which provides a distributed, fault-tolerant, and scalable platform for handling high volumes of real-time data.

Producers: Programs that receive raw exchange data via WebSockets, parse and normalize OB events, and publish those events to Kafka topics based on the symbol being traded. The system supports sharding by symbol using Kafka topic partitions, allowing for efficient storage and retrieval of OB data.

To map symbols to their corresponding partitions, the system uses JSON configuration files. For example, the binance-config.json file might look like this:
```
{
  "btcusdt": 0,
  "apeusdt": 1
}
```
This file maps the btcusdt symbol to partition 0 and the apeusdt symbol to partition 1 under the binance-orderbook topic. Consumers can subscribe to the specific partitions they are interested in based on the symbol they want to trade.

Broker: The Kafka message broker that handles the distribution and storage of the OB events.

Consumers :  Programs that listens to the Kafka topic (for example, binance-orderbook) and then listen to specific symbols by consuming data from the partitions defined in the partition maps of the JSON config file. The received data is used to create an order book in memory and generate signals for trading decisions.

For best latency, it is recommended to run the producers(Distributed exchange connectors) in AWS regions where the specific crypto exchange is located. This will minimize network latency and ensure timely delivery of real-time market data.

## Running the System

Before running the producers and consumers, you need to start the Kafka broker and ZooKeeper on your local machine. In this case, both Kafka broker and ZooKeeper can be run on the localhost. However, if you choose to run the brokers on a different machine, you can provide the machine's IP address instead of localhost.






