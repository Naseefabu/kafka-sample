
# Event-Driven Algorithmic Trading using Kafka
This project is an event-driven algorithmic trading system sample implementation using Kafka. The system receives raw exchange data via WebSockets, parses and normalizes order book (OB) events, and publishes those events via Kafka topics. Consumers (strategies) read from these topics, build the order book, create signals, and place orders. Additionally, the system uses separate JSON files containing partition maps for each symbol to allow consumers to subscribe to specific symbols of interest.


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