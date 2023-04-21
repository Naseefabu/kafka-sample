from kafka import KafkaAdminClient, KafkaConsumer
from kafka import TopicPartition
import json

# ("binance",btcusdt) => symbols should be exactly the same as in the config file
def get_orderbook_datafeed(exchange, symbol): 
    if(exchange == "binance"):
        with open('binance_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in binance exchange is not found. Please input valid symbol")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking-binance',
                            auto_offset_reset='latest'
                            )
        topic = "binance"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    
    elif (exchange == "coinbase"):
        with open('coinbase_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in coinbase exchange is not found. Please input valid symbol")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking-coinbase', 
                            auto_offset_reset='latest'
                            )
        topic = "coinbase"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "kraken"):
        with open('kraken_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in kraken exchange is not found. Please input valid symbol")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking-kraken', # fix ?
                            auto_offset_reset='latest'
                            )
        topic = "kraken"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "bitmex"):
        with open('bitmex_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in bitmex exchange is not found. Please input valid symbol")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking-bitmex', # fix ?
                            auto_offset_reset='latest'
                            )
        topic = "bitmex"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "bybit"):
        with open('bybit_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in bybit exchange is not found. Please input valid symbol")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking-bybit', # fix ?
                            auto_offset_reset='latest'
                            )
        topic = "bybit"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    else:
        raise RuntimeError("Exchange connector is not implemented. Please input valid exchange name")   