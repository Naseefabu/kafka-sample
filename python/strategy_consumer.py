from kafka import KafkaAdminClient, KafkaConsumer
from kafka import TopicPartition
import multiprocessing
import json


def test():
    consumer = KafkaConsumer(              
        bootstrap_servers=['localhost:9092'],
        group_id="strategy-three",           
        auto_offset_reset='earliest',  

    )

    # assign to a specific partition of the topic
    partition = TopicPartition('binance-orderbook', 1)
    consumer.assign([partition])

    # seek to the beginning of the partition
    consumer.seek_to_beginning(partition)

    for msg in consumer:
        print("binance orderbook = {}".format(json.loads(msg.value)))


# ("binance",btcusdt) => symbols should be exactly the same as in the config file
def get_orderbook_datafeed(exchange, symbol): 
    if(exchange == "binance"):
        with open('binance_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        if symbol not in symbol_dict.keys():
            raise RuntimeError("Symbol in binance exchange is not found. Please input valid symbol")
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking-binance', # fix ?
                            auto_offset_reset='earliest'
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
                            group_id='strategy-marketmaking-coinbase', # fix ?
                            auto_offset_reset='earliest'
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
                            auto_offset_reset='earliest'
                            )
        topic = "kraken"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    else:
        raise RuntimeError("Exchange connector is not implemented. Please input valid exchange name")   

    
class market_making:
    def __init__(self, bidspread, askspread, exchange, symbol):
        print("starting the strategy")
        # symbols it listening to
        self.symbol = symbol # symbol its market making
        self.exchange = exchange # exchange its market making
        self.bid_spread = bidspread
        self.ask_spread = askspread
        self.datafeed = get_orderbook_datafeed(exchange,symbol) # returns kafka consumer object 

    def run(self):
        for msg in self.datafeed:
            val = 0
            print(msg.value)
            print("consuming the market data from {} symbol {}".format(self.exchange,self.symbol))


def main():
    mm_strategy = market_making(1,2,"kraken","AUD/USD")
    p = multiprocessing.Process(target=mm_strategy.run)
    p.start()
    p.join()


main()