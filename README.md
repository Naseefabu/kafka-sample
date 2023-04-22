
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
    
  binance_config.json
  ```
  {
    "SOL/USDT": 0,
    "APE/USD": 1
  }
  ```
  This file maps the btcusdt symbol to partition 0 and the apeusdt symbol to partition 1 under the binance-orderbook topic. Consumers can subscribe to the specific partitions they are interested in based on the symbol they want to trade.

  The symbols partition maps is an essential aspect of this project. It's like a JSON file inside the project directory that tells you which partition ID does a specific symbol takes in a particular topic. For example, in the binance-orderbook topic, we may have a lot of partitions based on symbols in the Binance exchange, so the partition map will tell you what symbol and its partition ID so that consumers can identify them easily.

  ### Step 3: Start Producers and Consumers

  1. Run the producers, such as binance_producer.py, coinbase_producer.py, and bitmex_producer.py. For best performance, it is recommended to run these producers in their own AWS regions where the exchange servers are located.
  2. Run the consumers (strategies) to subscribe to specific symbols of interest and build the order book, create signals, and place orders.

  ## Kafka Topic Format

  1. The orderbook topic format for each exchange is as follows:

    ```
    exchangename-orderbook
    ```

  For example :

    ```
    binance-orderbook
    coinbase-orderbook
    bitmex-orderbook
    ```

  2. Each topic may have multiple partitions based on the symbols interested in that exchange.



## Architecture Overview

### Producers

  Producers (e.g., binance_producer.py, coinbase_producer.py) in this project use a multiprocessing approach based on the number of cores available on the machine. Instead of creating a separate process for each symbol's WebSocket subscription, we create one process per core, with each process having a single big event loop where specific symbols' WebSocket tasks are run. This approach allows us to distribute the workload across multiple cores and take full advantage of the available hardware resources. Additionally, we set the process core affinity to avoid context switch overheads, which further improves the performance of the producers.

  For best latency, it is recommended to run the producers(Distributed  exchange connectors) in AWS regions where the specific crypto exchange is located. This will minimize network latency and ensure timely delivery of real-time market data.








