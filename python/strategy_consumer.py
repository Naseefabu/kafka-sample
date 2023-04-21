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
def subscribe_orderbook(exchange, symbol): # check the symbol ?
    if(exchange == "binance"):
        with open('binance_config.json') as f:
            data = json.load(f)
        symbol_dict = {symbol: number for symbol, number in data.items()}
        consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                            group_id='strategy-marketmaking', # fix ?
                            auto_offset_reset='earliest'
                            )
        topic = "binance"+"-orderbook"
        partition = TopicPartition(topic, symbol_dict[symbol])
        consumer.assign([partition])
        return consumer
    else:
        raise RuntimeError("Exchange connector is not implemented")

    
class market_making:
    def __init__(self, bidspread, askspread, exchange, symbol):
        # symbols it listening to
        self.symbol = symbol # symbol its market making
        self.exchange = exchange # exchange its market making
        self.bid_spread = bidspread
        self.ask_spread = askspread
        self.datafeed = subscribe_orderbook(exchange,symbol) # returns kafka consumer object 

    def run(self):
        print("starting the strategy")
        while True:
            for msg in self.datafeed:
                print(msg.value)



def main():
    mm_strategy = market_making(1,2,"binance","apeusdt")
    p = multiprocessing.Process(target=mm_strategy.run)
    p.start()
    p.join()


main()