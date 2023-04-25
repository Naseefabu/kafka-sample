from confluent_kafka import Consumer, TopicPartition
import json

def get_orderbook_datafeed(exchange, symbol): 
    if(exchange == "binance"):
        with open('binance_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in binance exchange is not found. Please input valid symbol")
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'strategy-marketmaking-binance',
            'enable.auto.commit': False,
            'auto.offset.reset': 'latest',
            'max.poll.records': 1
        }

        consumer = Consumer(conf)

        # Assign to specific partitions of a topic
        topic_name = 'binance-orderbook'
        partition = TopicPartition(topic_name, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    
    elif (exchange == "coinbase"):
        with open('coinbase_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in coinbase exchange is not found. Please input valid symbol")
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'strategy-marketmaking-coinbase',
            'enable.auto.commit': False,
            'auto.offset.reset': 'latest',
            'max.poll.records': 1
        }

        consumer = Consumer(conf)

        # Assign to specific partitions of a topic
        topic_name = 'coinbase-orderbook'
        partition = TopicPartition(topic_name, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "kraken"):
        with open('kraken_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in kraken exchange is not found. Please input valid symbol")
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'strategy-marketmaking-kraken',
            'enable.auto.commit': False,
            'auto.offset.reset': 'latest',
            'max.poll.records': 1
        }

        consumer = Consumer(conf)

        # Assign to specific partitions of a topic
        topic_name = 'kraken-orderbook'
        partition = TopicPartition(topic_name, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "bitmex"):
        with open('bitmex_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in bitmex exchange is not found. Please input valid symbol")
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'strategy-marketmaking-bitmex',
            'enable.auto.commit': False,
            'auto.offset.reset': 'latest',
            'max.poll.records': 1
        }

        consumer = Consumer(conf)

        # Assign to specific partitions of a topic
        topic_name = 'bitmex-orderbook'
        partition = TopicPartition(topic_name, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "bybit"):
        with open('bybit_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in bybit exchange is not found. Please input valid symbol")
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'strategy-marketmaking-bybit',
            'enable.auto.commit': False,
            'auto.offset.reset': 'latest',
            'max.poll.records': 1
        }

        consumer = Consumer(conf)

        # Assign to specific partitions of a topic
        topic_name = 'bybit-orderbook'
        partition = TopicPartition(topic_name, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "bitfinex"):
        with open('bitfinex_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in bitfinex exchange is not found. Please input valid symbol")
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'strategy-marketmaking-bitfinex',
            'enable.auto.commit': False,
            'auto.offset.reset': 'latest',
            'max.poll.records': 1
        }

        consumer = Consumer(conf)

        # Assign to specific partitions of a topic
        topic_name = 'bitfinex-orderbook'
        partition = TopicPartition(topic_name, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    else:
        raise RuntimeError("Exchange connector is not implemented. Please input valid exchange name") 