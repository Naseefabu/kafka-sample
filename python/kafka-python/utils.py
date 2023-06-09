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
                            enable_auto_commit=False,
                            auto_offset_reset='latest', # reads latest snapshot value only
                            max_poll_records=1 # one at a time
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
                            enable_auto_commit=False,
                            auto_offset_reset='latest', # reads latest snapshot value only
                            max_poll_records=1 # one at a time
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
                            group_id='strategy-marketmaking-kraken', 
                            enable_auto_commit=False,
                            auto_offset_reset='latest', # reads latest snapshot value only
                            max_poll_records=1 # one at a time
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
                            group_id='strategy-marketmaking-bitmex', 
                            enable_auto_commit=False,
                            auto_offset_reset='latest', # reads latest snapshot value only
                            max_poll_records=1 # one at a time
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
                            group_id='strategy-marketmaking-bybit', 
                            enable_auto_commit=False,
                            auto_offset_reset='latest', # reads latest snapshot value only
                            max_poll_records=1 # one at a time
                            )
        topic = "bybit"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    elif (exchange == "bitfinex"):
        with open('bitfinex_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in bitfinex exchange is not found. Please input valid symbol")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking-bitfinex', 
                            enable_auto_commit=False,
                            auto_offset_reset='latest', # reads latest snapshot value only
                            max_poll_records=1, # one at a time
                            )
        topic = "bitfinex"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    else:
        raise RuntimeError("Exchange connector is not implemented. Please input valid exchange name")   
    

