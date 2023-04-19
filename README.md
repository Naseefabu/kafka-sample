




# instructions




# misc

download apache : https://kafka.apache.org/
sudo apt update

Every broker on a Kafka cluster is also named a Bootstrap Server. All brokers have the metadata required for the clients (producer or consumer) to discover brokers. When a client connects to one of the brokers (which are already configured as bootstrap servers in the Kafka configuration) it makes a "metadata request". The response includes information about topics, partitions, leader brokers, etc. Once the client gets this info, then - in the case of a producer- it makes the write request directly to the leader broker for that specific partition.



Topics:

Topic : binance-trade
Partitions : symbols

Topic : binance-orderbook
Partitions : symbols

Topic : binance-delta
Partitions : symbols

Topic : coinbase-trade
Partitions : symbols

Topic : coinbase-orderbook
Partitions : symbols

Topic : coinbase-delta
Partitions : symbols

Topic : kraken-trade
Partitions : symbols

Topic : kraken-orderbook
Partitions : symbols

Topic : kraken-delta
Partitions : symbols



Run the consumer first 